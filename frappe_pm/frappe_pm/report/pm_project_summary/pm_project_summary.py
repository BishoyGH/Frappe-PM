import frappe
from frappe import _


def execute(filters=None):
    rows = frappe.get_list(
        "PM Project",
        filters={"is_archived": 0},
        fields=[
            "name",
            "project_name",
            "status",
            "health",
            "percent_complete",
            "total_tasks",
            "completed_tasks",
            "budget",
            "actual_cost",
            "end_date",
        ],
        order_by="modified desc",
    )
    columns = [
        {
            "label": _("Project"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "PM Project",
            "width": 140,
        },
        {"label": _("Name"), "fieldname": "project_name", "fieldtype": "Data", "width": 200},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 90},
        {"label": _("Health"), "fieldname": "health", "fieldtype": "Data", "width": 80},
        {"label": _("% Complete"), "fieldname": "percent_complete", "fieldtype": "Percent", "width": 100},
        {"label": _("Tasks"), "fieldname": "total_tasks", "fieldtype": "Int", "width": 70},
        {"label": _("Done"), "fieldname": "completed_tasks", "fieldtype": "Int", "width": 70},
        {"label": _("Budget"), "fieldname": "budget", "fieldtype": "Currency", "width": 110},
        {"label": _("Actual Cost"), "fieldname": "actual_cost", "fieldtype": "Currency", "width": 110},
        {"label": _("Planned End"), "fieldname": "end_date", "fieldtype": "Date", "width": 100},
    ]
    return columns, rows
