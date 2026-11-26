import frappe
from frappe import _
from frappe.utils import add_days, add_months, getdate, nowdate
from frappe.utils.nestedset import NestedSet

from frappe_pm.graph import has_cycle

CLOSED = ("Completed", "Cancelled")


class PMTask(NestedSet):
    nsm_parent_field = "parent_pm_task"

    def validate(self):
        self.validate_dates()
        self.validate_parent()
        self.validate_dependencies()
        self.sync_status_progress()
        self.is_overdue = int(
            bool(self.due_date) and self.status not in CLOSED and getdate(self.due_date) < getdate(nowdate())
        )

    def validate_dates(self):
        if self.start_date and self.due_date and getdate(self.due_date) < getdate(self.start_date):
            frappe.throw(_("Due Date cannot be before Start Date"))

    def validate_parent(self):
        if self.parent_pm_task:
            if self.parent_pm_task == self.name:
                frappe.throw(_("A task cannot be its own parent"))
            parent_project = frappe.db.get_value("PM Task", self.parent_pm_task, "project")
            if parent_project != self.project:
                frappe.throw(_("Parent task must belong to the same project"))

    def validate_dependencies(self):
        for dep in self.depends_on:
            if dep.depends_on_task == self.name:
                frappe.throw(_("A task cannot depend on itself"))
        if not self.name or self.is_new() or not self.depends_on:
            return
        edges = {self.name: [d.depends_on_task for d in self.depends_on]}
        for row in frappe.get_all(
            "PM Task Dependency", fields=["parent", "depends_on_task"], filters={"parenttype": "PM Task"}
        ):
            if row.parent != self.name:
                edges.setdefault(row.parent, []).append(row.depends_on_task)
        if has_cycle(edges, self.name):
            frappe.throw(_("Circular dependency detected"))

    def sync_status_progress(self):
        if self.status == "Completed":
            self.progress = 100
            self.completed_on = self.completed_on or nowdate()
        else:
            self.completed_on = None
            if self.status == "Open" and not self.progress and self.checklist:
                done = sum(1 for c in self.checklist if c.done)
                self.progress = done / len(self.checklist) * 100

    def before_save(self):
        if self.status == "Completed" and self.is_group:
            open_children = frappe.db.count(
                "PM Task", {"parent_pm_task": self.name, "status": ["not in", list(CLOSED)]}
            )
            if open_children:
                frappe.throw(_("Complete all subtasks first"))

    def on_update(self):
        super().on_update()
        self.rollup_parent()
        self.refresh_project()
        if self.has_value_changed("status") and self.status == "Completed" and self.is_recurring:
            self.spawn_next_occurrence()

    def on_trash(self):
        super().on_trash()
        self.refresh_project()

    def rollup_parent(self):
        if not self.parent_pm_task:
            return
        sibs = frappe.get_all(
            "PM Task",
            filters={"parent_pm_task": self.parent_pm_task, "status": ["!=", "Cancelled"]},
            fields=["status", "progress"],
        )
        if not sibs:
            return
        progress = sum(s.progress or 0 for s in sibs) / len(sibs)
        frappe.db.set_value("PM Task", self.parent_pm_task, "progress", progress, update_modified=False)

    def refresh_project(self):
        if self.project and frappe.db.exists("PM Project", self.project):
            proj = frappe.get_doc("PM Project", self.project)
            proj.update_rollups()
            proj.db_set(
                {
                    "total_tasks": proj.total_tasks,
                    "completed_tasks": proj.completed_tasks,
                    "percent_complete": proj.percent_complete,
                    "estimated_hours": proj.estimated_hours,
                    "actual_hours": proj.actual_hours,
                    "health": proj.health,
                },
                update_modified=False,
            )

    def spawn_next_occurrence(self):
        if not self.recurrence:
            return
        step = {
            "Daily": lambda d: add_days(d, 1),
            "Weekly": lambda d: add_days(d, 7),
            "Monthly": lambda d: add_months(d, 1),
        }[self.recurrence]
        nxt = step(self.due_date or nowdate())
        if self.recurrence_end and getdate(nxt) > getdate(self.recurrence_end):
            return
        new = frappe.copy_doc(self)
        new.status = "Open"
        new.progress = 0
        new.completed_on = None
        new.start_date = step(self.start_date) if self.start_date else None
        new.due_date = nxt
        new.insert(ignore_permissions=True)


def get_children(doctype, parent="", project=None, is_root=False, **filters):
    return frappe.get_all(
        "PM Task",
        fields=["name as value", "subject as title", "is_group as expandable"],
        filters={
            "parent_pm_task": ["=", parent or ""] if not is_root else ["is", "not set"],
            **({"project": project} if project else {}),
        },
        order_by="backlog_rank asc, creation asc",
    )


@frappe.whitelist()
def set_status(task, status):
    doc = frappe.get_doc("PM Task", task)
    doc.check_permission("write")
    doc.status = status
    doc.save()
    return doc.status
