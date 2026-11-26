import frappe
from frappe import _
from frappe.utils import date_diff, nowdate


def execute(filters=None):
    filters = filters or {}
    cond = {"status": ["not in", ["Completed", "Cancelled"]], "due_date": ["<", nowdate()]}
    if filters.get("project"):
        cond["project"] = filters["project"]
    rows = frappe.get_list(
        "PM Task",
        filters=cond,
        fields=["name", "subject", "project", "status", "priority", "due_date", "_assign"],
        order_by="due_date asc",
    )
    for r in rows:
        r["days_overdue"] = date_diff(nowdate(), r.due_date)
    columns = [
        {"label": _("Task"), "fieldname": "name", "fieldtype": "Link", "options": "PM Task", "width": 120},
        {"label": _("Subject"), "fieldname": "subject", "fieldtype": "Data", "width": 240},
        {
            "label": _("Project"),
            "fieldname": "project",
            "fieldtype": "Link",
            "options": "PM Project",
            "width": 140,
        },
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": _("Priority"), "fieldname": "priority", "fieldtype": "Data", "width": 90},
        {"label": _("Due Date"), "fieldname": "due_date", "fieldtype": "Date", "width": 100},
        {"label": _("Days Overdue"), "fieldname": "days_overdue", "fieldtype": "Int", "width": 100},
    ]
    return columns, rows
