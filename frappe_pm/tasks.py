"""Scheduled jobs."""

import frappe
from frappe.utils import nowdate


def daily():
    mark_overdue_tasks()
    refresh_project_health()


def mark_overdue_tasks():
    today = nowdate()
    frappe.db.sql(
        """update `tabPM Task` set is_overdue = 1
		where due_date < %s and status not in ('Completed','Cancelled') and is_overdue = 0""",
        today,
    )
    frappe.db.sql(
        """update `tabPM Task` set is_overdue = 0
		where is_overdue = 1 and (status in ('Completed','Cancelled') or due_date is null or due_date >= %s)""",
        today,
    )


def refresh_project_health():
    for name in frappe.get_all(
        "PM Project", filters={"status": ["in", ["Planning", "Active"]]}, pluck="name"
    ):
        doc = frappe.get_doc("PM Project", name)
        doc.update_rollups()
        doc.db_set({"health": doc.health, "percent_complete": doc.percent_complete}, update_modified=False)
