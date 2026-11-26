import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate


class PMSprint(Document):
    def validate(self):
        if getdate(self.end_date) < getdate(self.start_date):
            frappe.throw(_("End Date cannot be before Start Date"))
        if self.status == "Active":
            other = frappe.db.exists(
                "PM Sprint", {"project": self.project, "status": "Active", "name": ["!=", self.name]}
            )
            if other:
                frappe.throw(_("Project already has an active sprint: {0}").format(other))
        self.update_metrics()

    def update_metrics(self):
        if self.is_new():
            return
        r = frappe.db.sql(
            """select count(*), sum(status='Completed'), coalesce(sum(story_points),0),
			coalesce(sum(case when status='Completed' then story_points else 0 end),0)
			from `tabPM Task` where sprint = %s and status != 'Cancelled'""",
            self.name,
        )[0]
        self.total_tasks, self.completed_tasks = r[0] or 0, int(r[1] or 0)
        self.committed_points, self.completed_points = r[2], r[3]


@frappe.whitelist()
def complete_sprint(sprint, move_incomplete_to=None):
    """Complete a sprint; unfinished tasks go to another sprint or back to the backlog."""
    doc = frappe.get_doc("PM Sprint", sprint)
    doc.check_permission("write")
    for t in frappe.get_all(
        "PM Task", filters={"sprint": sprint, "status": ["not in", ["Completed", "Cancelled"]]}, pluck="name"
    ):
        frappe.db.set_value(
            "PM Task",
            t,
            {"sprint": move_incomplete_to or None, "status": "Open" if move_incomplete_to else "Backlog"},
        )
    doc.status = "Completed"
    doc.save()
    return doc.name


@frappe.whitelist()
def burndown(sprint):
    """Return daily remaining points based on task completion dates."""
    from frappe.utils import add_days

    doc = frappe.get_doc("PM Sprint", sprint)
    tasks = frappe.get_all(
        "PM Task",
        filters={"sprint": sprint, "status": ["!=", "Cancelled"]},
        fields=["story_points", "completed_on"],
    )
    total = sum(t.story_points or 0 for t in tasks)
    out, day = [], getdate(doc.start_date)
    while day <= getdate(doc.end_date):
        done = sum((t.story_points or 0) for t in tasks if t.completed_on and getdate(t.completed_on) <= day)
        out.append({"date": str(day), "remaining": total - done})
        day = getdate(add_days(day, 1))
    return {"total": total, "series": out}
