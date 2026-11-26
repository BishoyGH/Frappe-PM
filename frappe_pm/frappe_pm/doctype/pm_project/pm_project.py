import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class PMProject(Document):
    def validate(self):
        self.validate_dates()
        self.validate_members()
        self.update_rollups()

    def validate_dates(self):
        if self.start_date and self.end_date and getdate(self.end_date) < getdate(self.start_date):
            frappe.throw(_("Planned End Date cannot be before Start Date"))

    def validate_members(self):
        seen = set()
        for m in self.members:
            if m.user in seen:
                frappe.throw(_("User {0} is added more than once").format(m.user))
            seen.add(m.user)

    def update_rollups(self):
        if self.is_new():
            return
        row = frappe.db.sql(
            """select count(*), sum(status = 'Completed'), coalesce(sum(estimated_hours),0),
				coalesce(sum(actual_hours),0), coalesce(avg(progress),0)
			from `tabPM Task` where project = %s and status != 'Cancelled' and is_group = 0""",
            self.name,
        )[0]
        self.total_tasks = row[0] or 0
        self.completed_tasks = int(row[1] or 0)
        self.estimated_hours = row[2]
        self.actual_hours = row[3]
        self.percent_complete = (self.completed_tasks / self.total_tasks * 100) if self.total_tasks else 0
        self.health = self.compute_health()
        if self.status == "Active" and not self.actual_start_date:
            self.actual_start_date = nowdate()
        if self.status == "Completed" and not self.actual_end_date:
            self.actual_end_date = nowdate()

    def compute_health(self):
        if self.status in ("Completed", "Cancelled"):
            return "Green"
        overdue = frappe.db.count("PM Task", {"project": self.name, "is_overdue": 1})
        late = bool(self.end_date) and getdate(self.end_date) < getdate(nowdate())
        over_budget = bool(self.budget) and (self.actual_cost or 0) > self.budget
        if late or over_budget or overdue >= 5:
            return "Red"
        if overdue or (self.budget and (self.actual_cost or 0) > 0.9 * self.budget):
            return "Amber"
        return "Green"

    @frappe.whitelist()
    def archive(self):
        self.db_set("is_archived", 1)

    @frappe.whitelist()
    def restore(self):
        self.db_set("is_archived", 0)


@frappe.whitelist()
def create_from_template(template, project_name, start_date=None):
    """Create a project and its tasks from a PM Project Template."""
    from frappe_pm.utils import add_working_days

    frappe.has_permission("PM Project", "create", throw=True)
    tpl = frappe.get_doc("PM Project Template", template)
    start = getdate(start_date or nowdate())
    project = frappe.get_doc(
        {
            "doctype": "PM Project",
            "project_name": project_name,
            "project_type": tpl.project_type,
            "start_date": start,
            "template": tpl.name,
        }
    ).insert()
    for row in tpl.tasks:
        s = add_working_days(start, row.offset_days or 0)
        frappe.get_doc(
            {
                "doctype": "PM Task",
                "subject": row.subject,
                "project": project.name,
                "task_type": row.task_type,
                "priority": row.priority,
                "start_date": s,
                "due_date": add_working_days(s, max((row.duration_days or 1) - 1, 0)),
                "estimated_hours": row.estimated_hours,
            }
        ).insert()
    return project.name
