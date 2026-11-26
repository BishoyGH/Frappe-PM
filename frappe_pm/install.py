import frappe

ROLES = ["PM Admin", "Project Manager", "Team Member", "PM Viewer", "PM Client"]


def after_install():
    for role in ROLES:
        if not frappe.db.exists("Role", role):
            frappe.get_doc(
                {"doctype": "Role", "role_name": role, "desk_access": 1 if role != "PM Client" else 0}
            ).insert(ignore_permissions=True)
    if not frappe.db.exists("PM Activity Type", "Development"):
        for name, billable in (
            ("Development", 1),
            ("Design", 1),
            ("Meeting", 0),
            ("Review", 1),
            ("Admin", 0),
        ):
            frappe.get_doc(
                {"doctype": "PM Activity Type", "activity_type": name, "billable": billable}
            ).insert(ignore_permissions=True)
    if not frappe.db.exists("PM Project Type", "Internal"):
        for name in ("Internal", "Client", "R&D", "Support"):
            frappe.get_doc({"doctype": "PM Project Type", "project_type": name}).insert(
                ignore_permissions=True
            )
    frappe.db.commit()
