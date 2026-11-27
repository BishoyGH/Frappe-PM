"""Whitelisted REST API (``/api/method/frappe_pm.api.<name>``)."""

import frappe
from frappe import _
from frappe.utils import cint


@frappe.whitelist()
def my_tasks(include_closed=0):
    """Tasks assigned to the current user via Frappe's assignment system."""
    names = frappe.get_all(
        "ToDo",
        filters={"allocated_to": frappe.session.user, "reference_type": "PM Task", "status": "Open"},
        pluck="reference_name",
    )
    flt = {"name": ["in", names or [""]]}
    if not cint(include_closed):
        flt["status"] = ["not in", ["Completed", "Cancelled"]]
    return frappe.get_list(
        "PM Task",
        filters=flt,
        fields=["name", "subject", "project", "status", "priority", "due_date", "progress"],
        order_by="due_date asc",
    )


@frappe.whitelist()
def project_overview(project):
    doc = frappe.get_doc("PM Project", project)
    doc.check_permission("read")
    by_status = frappe.db.sql(
        "select status, count(*) as count from `tabPM Task` where project=%s group by status",
        project,
        as_dict=True,
    )
    return {
        "project": doc.name,
        "name": doc.project_name,
        "status": doc.status,
        "health": doc.health,
        "percent_complete": doc.percent_complete,
        "tasks_by_status": by_status,
        "milestones": frappe.get_all(
            "PM Milestone",
            filters={"project": project},
            fields=["name", "milestone_name", "status", "due_date"],
        ),
        "open_risks": frappe.db.count(
            "PM Risk", {"project": project, "status": ["in", ["Open", "Mitigating"]]}
        ),
        "open_issues": frappe.db.count(
            "PM Issue", {"project": project, "status": ["in", ["Open", "In Progress"]]}
        ),
    }


@frappe.whitelist()
def bulk_update_tasks(tasks, values):
    """Apply the same field values to many tasks. ``tasks``: list of names, ``values``: dict."""
    tasks, values = frappe.parse_json(tasks), frappe.parse_json(values)
    allowed = {"status", "priority", "sprint", "epic", "milestone", "due_date", "start_date"}
    bad = set(values) - allowed
    if bad:
        frappe.throw(_("Fields not allowed in bulk update: {0}").format(", ".join(sorted(bad))))
    updated = []
    for name in tasks:
        doc = frappe.get_doc("PM Task", name)
        doc.check_permission("write")
        doc.update(values)
        doc.save()
        updated.append(name)
    return updated


@frappe.whitelist()
def log_time(project, hours, task=None, notes=None, billable=1):
    """Quick time entry: creates a draft timesheet for today ending now."""
    from frappe.utils import add_to_date, now_datetime

    end = now_datetime()
    ts = frappe.get_doc(
        {
            "doctype": "PM Timesheet",
            "user": frappe.session.user,
            "time_logs": [
                {
                    "project": project,
                    "task": task,
                    "hours": float(hours),
                    "from_time": add_to_date(end, hours=-float(hours)),
                    "to_time": end,
                    "billable": cint(billable),
                    "notes": notes,
                }
            ],
        }
    ).insert()
    return ts.name
