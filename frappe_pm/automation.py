"""Tiny rule engine: PM Automation Rule rows run on PM Task events."""

import frappe


def _rules(event, doc):
    rules = frappe.get_all(
        "PM Automation Rule",
        filters={"enabled": 1, "trigger_event": event},
        fields=["name", "project", "condition_status", "action", "action_value"],
    )
    return [
        r
        for r in rules
        if (not r.project or r.project == doc.project)
        and (not r.condition_status or r.condition_status == doc.status)
    ]


def apply(rule, doc):
    a, v = rule["action"], rule["action_value"]
    if a == "Set Status":
        doc.db_set("status", v)
    elif a == "Set Priority":
        doc.db_set("priority", v)
    elif a == "Assign To":
        from frappe.desk.form.assign_to import add

        add({"doctype": "PM Task", "name": doc.name, "assign_to": [v]})
    elif a == "Add Comment":
        doc.add_comment("Comment", v)
    elif a == "Notify User":
        frappe.publish_realtime("msgprint", f"Automation: {doc.name} - {v}", user=v)


def on_task_created(doc, method=None):
    for r in _rules("Task Created", doc):
        apply(r, doc)


def on_task_update(doc, method=None):
    if doc.flags.in_automation:
        return
    doc.flags.in_automation = True
    if doc.has_value_changed("status"):
        for r in _rules("Task Status Changed", doc):
            apply(r, doc)
        if doc.status == "Completed":
            unblock_dependents(doc)


def unblock_dependents(doc):
    for parent in frappe.get_all("PM Task Dependency", filters={"depends_on_task": doc.name}, pluck="parent"):
        open_deps = frappe.db.sql(
            """select count(*) from `tabPM Task Dependency` d join `tabPM Task` t on t.name = d.depends_on_task
            where d.parent = %s and t.status not in ('Completed','Cancelled')""",
            parent,
        )[0][0]
        if not open_deps and frappe.db.get_value("PM Task", parent, "status") == "Blocked":
            frappe.db.set_value("PM Task", parent, "status", "Open")
            for r in _rules("Dependency Completed", frappe.get_doc("PM Task", parent)):
                apply(r, frappe.get_doc("PM Task", parent))
