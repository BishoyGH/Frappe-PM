"""Row-level visibility: privileged roles see everything, others only projects they belong to."""

import frappe

PRIVILEGED = {"System Manager", "PM Admin", "Project Manager"}


def _privileged(user):
    return user == "Administrator" or bool(PRIVILEGED & set(frappe.get_roles(user)))


def _member_projects(user):
    rows = frappe.get_all(
        "PM Project Member", filters={"user": user, "parenttype": "PM Project"}, pluck="parent"
    )
    owned = frappe.get_all("PM Project", filters={"project_manager": user}, pluck="name")
    return list(set(rows) | set(owned))


def project_query(user=None):
    user = user or frappe.session.user
    if _privileged(user):
        return ""
    names = _member_projects(user)
    cond = (
        "`tabPM Project`.is_private = 0"
        if not names
        else (
            "(`tabPM Project`.is_private = 0 or `tabPM Project`.name in ({}))".format(
                ", ".join(frappe.db.escape(n) for n in names)
            )
        )
    )
    return cond


def task_query(user=None):
    user = user or frappe.session.user
    if _privileged(user):
        return ""
    names = _member_projects(user)
    public = frappe.get_all("PM Project", filters={"is_private": 0}, pluck="name")
    allowed = list(set(names) | set(public))
    if not allowed:
        return "1=0"
    return "`tabPM Task`.project in ({})".format(", ".join(frappe.db.escape(n) for n in allowed))


def has_project_permission(doc, user=None, permission_type=None):
    user = user or frappe.session.user
    if _privileged(user) or not doc.is_private:
        return True
    return doc.name in _member_projects(user)


def has_task_permission(doc, user=None, permission_type=None):
    user = user or frappe.session.user
    if _privileged(user) or not doc.project:
        return True
    project = frappe.db.get_value("PM Project", doc.project, ["is_private"], as_dict=True)
    if not project or not project.is_private:
        return True
    return doc.project in _member_projects(user)
