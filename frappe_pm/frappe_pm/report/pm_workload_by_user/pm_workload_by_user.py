import frappe
from frappe import _


def execute(filters=None):
    rows = frappe.db.sql(
        """select todo.allocated_to as user, count(*) as open_tasks,
            coalesce(sum(t.estimated_hours), 0) as estimated_hours, coalesce(sum(t.story_points), 0) as story_points
        from `tabToDo` todo join `tabPM Task` t on t.name = todo.reference_name
        where todo.reference_type = 'PM Task' and todo.status = 'Open' and t.status not in ('Completed','Cancelled')
        group by todo.allocated_to order by open_tasks desc""",
        as_dict=True,
    )
    columns = [
        {"label": _("User"), "fieldname": "user", "fieldtype": "Link", "options": "User", "width": 200},
        {"label": _("Open Tasks"), "fieldname": "open_tasks", "fieldtype": "Int", "width": 100},
        {"label": _("Estimated Hours"), "fieldname": "estimated_hours", "fieldtype": "Float", "width": 130},
        {"label": _("Story Points"), "fieldname": "story_points", "fieldtype": "Float", "width": 110},
    ]
    chart = {
        "data": {
            "labels": [r.user for r in rows],
            "datasets": [{"name": _("Open Tasks"), "values": [r.open_tasks for r in rows]}],
        },
        "type": "bar",
    }
    return columns, rows, None, chart
