app_name = "frappe_pm"
app_title = "Frappe PM"
app_publisher = "Frappe PM Contributors"
app_description = "Project management for Frappe"
app_email = "noreply@example.com"
app_license = "MIT"

add_to_apps_screen = [
    {
        "name": "frappe_pm",
        "logo": "/assets/frappe_pm/images/logo.svg",
        "title": "Frappe PM",
        "route": "/app/frappe-pm",
    }
]

after_install = "frappe_pm.install.after_install"

fixtures = [
    {
        "dt": "Role",
        "filters": [["name", "in", ["PM Admin", "Project Manager", "Team Member", "PM Viewer", "PM Client"]]],
    }
]

doctype_js = {}

permission_query_conditions = {
    "PM Project": "frappe_pm.permissions.project_query",
    "PM Task": "frappe_pm.permissions.task_query",
}
has_permission = {
    "PM Project": "frappe_pm.permissions.has_project_permission",
    "PM Task": "frappe_pm.permissions.has_task_permission",
}

scheduler_events = {
    "daily": ["frappe_pm.tasks.daily"],
}

doc_events = {
    "PM Task": {
        "after_insert": "frappe_pm.automation.on_task_created",
        "on_update": "frappe_pm.automation.on_task_update",
    }
}
