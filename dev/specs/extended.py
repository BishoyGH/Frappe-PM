PRIORITY = "Low\nMedium\nHigh\nUrgent"
RAG = "Low\nMedium\nHigh\nCritical"


def named(name, series, title, fields, **kw):
    return dict(
        name=name,
        autoname="naming_series:",
        title=title,
        fields=[("naming_series", "Series", "Select", series, f"default={series}")] + fields,
        **kw,
    )


PROJ = ("project", "Project", "Link", "PM Project", "req,list,filter")
DESC = ("description", "Description", "Text Editor")
SPECS = [
    named(
        "PM Risk",
        "PM-RISK-.####",
        "title",
        [
            ("title", "Risk", "Data", None, "req,list"),
            PROJ,
            ("status", "Status", "Select", "Open\nMitigating\nClosed\nOccurred", "default=Open,list,filter"),
            ("probability", "Probability", "Select", RAG, "default=Medium"),
            ("impact", "Impact", "Select", RAG, "default=Medium"),
            ("score", "Score", "Int", None, "ro,list"),
            ("owner_user", "Owner", "Link", "User"),
            ("mitigation", "Mitigation Plan", "Text Editor"),
            DESC,
        ],
    ),
    named(
        "PM Issue",
        "PM-ISS-.####",
        "title",
        [
            ("title", "Issue", "Data", None, "req,list"),
            PROJ,
            ("status", "Status", "Select", "Open\nIn Progress\nResolved\nClosed", "default=Open,list,filter"),
            ("priority", "Priority", "Select", PRIORITY, "default=Medium,list,filter"),
            ("assigned_to", "Assigned To", "Link", "User"),
            ("related_task", "Related Task", "Link", "PM Task"),
            ("resolution", "Resolution", "Text Editor"),
            DESC,
        ],
    ),
    named(
        "PM Change Request",
        "PM-CR-.####",
        "title",
        [
            ("title", "Change Request", "Data", None, "req,list"),
            PROJ,
            (
                "status",
                "Status",
                "Select",
                "Draft\nPending Approval\nApproved\nRejected\nImplemented",
                "default=Draft,list,filter",
            ),
            ("requested_by", "Requested By", "Link", "User"),
            ("schedule_impact_days", "Schedule Impact (days)", "Int"),
            ("cost_impact", "Cost Impact", "Currency"),
            ("justification", "Justification", "Text Editor"),
            DESC,
        ],
        submittable=False,
    ),
    named(
        "PM Decision",
        "PM-DEC-.####",
        "title",
        [
            ("title", "Decision", "Data", None, "req,list"),
            PROJ,
            ("decided_on", "Decided On", "Date", None, "list"),
            ("decided_by", "Decided By", "Link", "User"),
            ("rationale", "Rationale", "Text Editor"),
            DESC,
        ],
    ),
    named(
        "PM Stakeholder",
        "PM-STK-.####",
        "stakeholder_name",
        [
            ("stakeholder_name", "Name", "Data", None, "req,list"),
            PROJ,
            ("email", "Email", "Data", "Email"),
            ("role", "Role", "Data", None, "list"),
            ("influence", "Influence", "Select", "Low\nMedium\nHigh"),
            ("interest", "Interest", "Select", "Low\nMedium\nHigh"),
            ("communication_plan", "Communication Plan", "Small Text"),
        ],
    ),
    named(
        "PM Status Update",
        "PM-UPD-.YYYY.-.####",
        "summary",
        [
            PROJ,
            ("summary", "Summary", "Data", None, "req,list"),
            ("health", "Health", "Select", "Green\nAmber\nRed", "default=Green,list"),
            ("posted_on", "Posted On", "Date", None, "default=Today,list"),
            ("accomplishments", "Accomplishments", "Text Editor"),
            ("next_steps", "Next Steps", "Text Editor"),
            ("blockers", "Blockers", "Text Editor"),
        ],
    ),
]
SPECS += [
    dict(
        name="PM Meeting Action Item",
        table=True,
        fields=[
            ("action", "Action", "Data", None, "req,list"),
            ("owner_user", "Owner", "Link", "User", "list"),
            ("due_date", "Due Date", "Date", None, "list"),
            ("task", "Created Task", "Link", "PM Task", "ro"),
        ],
    ),
    named(
        "PM Meeting Note",
        "PM-MTG-.YYYY.-.####",
        "title",
        [
            ("title", "Title", "Data", None, "req,list"),
            PROJ,
            ("meeting_date", "Date", "Datetime", None, "list"),
            ("meeting_url", "Meeting Link", "Data", "URL"),
            ("attendees", "Attendees", "Small Text"),
            ("agenda", "Agenda", "Text Editor"),
            ("notes", "Notes", "Text Editor"),
            ("actions", "Action Items", "Table", "PM Meeting Action Item"),
        ],
    ),
    named(
        "PM Retrospective",
        "PM-RET-.####",
        "title",
        [
            ("title", "Title", "Data", None, "req,list"),
            PROJ,
            ("sprint", "Sprint", "Link", "PM Sprint", "list"),
            ("went_well", "Went Well", "Text Editor"),
            ("to_improve", "To Improve", "Text Editor"),
            ("action_items", "Action Items", "Text Editor"),
        ],
    ),
    named(
        "PM Release",
        "PM-REL-.####",
        "version",
        [
            ("version", "Version", "Data", None, "req,list"),
            PROJ,
            ("status", "Status", "Select", "Planned\nIn Progress\nReleased", "default=Planned,list,filter"),
            ("release_date", "Release Date", "Date", None, "list"),
            ("release_notes", "Release Notes", "Text Editor"),
        ],
    ),
    named(
        "PM Announcement",
        "PM-ANN-.####",
        "title",
        [
            ("title", "Title", "Data", None, "req,list"),
            PROJ,
            ("pinned", "Pinned", "Check"),
            ("body", "Body", "Text Editor"),
        ],
    ),
    dict(
        name="PM Skill",
        autoname="field:skill_name",
        fields=[("skill_name", "Skill", "Data", None, "req,unique,list")],
    ),
    dict(
        name="PM Resource Skill",
        table=True,
        fields=[
            ("skill", "Skill", "Link", "PM Skill", "req,list"),
            (
                "proficiency",
                "Proficiency",
                "Select",
                "Beginner\nIntermediate\nAdvanced\nExpert",
                "default=Intermediate,list",
            ),
        ],
    ),
    dict(
        name="PM Resource Profile",
        autoname="field:user",
        fields=[
            ("user", "User", "Link", "User", "req,unique,list"),
            ("job_title", "Job Title", "Data", None, "list"),
            ("team", "Team", "Link", "PM Team", "filter"),
            ("weekly_capacity_hours", "Weekly Capacity (hours)", "Float", None, "default=40,list"),
            ("billing_rate", "Billing Rate", "Currency"),
            ("costing_rate", "Costing Rate", "Currency"),
            ("is_external", "External Contractor", "Check"),
            ("skills", "Skills", "Table", "PM Resource Skill"),
        ],
    ),
    named(
        "PM Resource Allocation",
        "PM-ALC-.####",
        "user",
        [
            ("user", "User", "Link", "User", "req,list,filter"),
            PROJ,
            ("start_date", "Start Date", "Date", None, "req,list"),
            ("end_date", "End Date", "Date", None, "req,list"),
            ("allocation_percent", "Allocation %", "Percent", None, "req,default=100,list"),
            ("hours_per_week", "Hours Per Week", "Float", None, "ro"),
        ],
    ),
    dict(
        name="PM Budget Line",
        table=True,
        fields=[
            (
                "category",
                "Category",
                "Select",
                "Labor\nSoftware\nHardware\nTravel\nVendor\nOther",
                "req,list",
            ),
            ("description", "Description", "Data", None, "list"),
            ("planned_amount", "Planned", "Currency", None, "req,list"),
            ("actual_amount", "Actual", "Currency", None, "list"),
        ],
    ),
    named(
        "PM Project Budget",
        "PM-BUD-.####",
        "project",
        [
            PROJ,
            ("status", "Status", "Select", "Draft\nPending Approval\nApproved", "default=Draft,list,filter"),
            ("lines", "Budget Lines", "Table", "PM Budget Line"),
            ("total_planned", "Total Planned", "Currency", None, "ro,list"),
            ("total_actual", "Total Actual", "Currency", None, "ro,list"),
            ("variance", "Variance", "Currency", None, "ro"),
            ("alert_threshold_percent", "Alert Threshold %", "Percent", None, "default=90"),
        ],
    ),
    named(
        "PM Baseline",
        "PM-BL-.####",
        "title",
        [
            ("title", "Title", "Data", None, "req,list"),
            PROJ,
            ("snapshot", "Snapshot (JSON)", "Code", "JSON", "ro"),
        ],
    ),
    named(
        "PM Automation Rule",
        "PM-AUTO-.####",
        "title",
        [
            ("title", "Rule", "Data", None, "req,list"),
            ("enabled", "Enabled", "Check", None, "default=1,list"),
            ("project", "Project (optional)", "Link", "PM Project"),
            (
                "trigger_event",
                "Trigger",
                "Select",
                "Task Created\nTask Status Changed\nTask Overdue\nDependency Completed",
                "req,list",
            ),
            (
                "condition_status",
                "When Status Is",
                "Select",
                "\nBacklog\nOpen\nIn Progress\nIn Review\nBlocked\nCompleted",
            ),
            (
                "action",
                "Action",
                "Select",
                "Set Status\nSet Priority\nAssign To\nNotify User\nAdd Comment",
                "req,list",
            ),
            ("action_value", "Action Value", "Data", None, "req"),
        ],
    ),
    named(
        "PM Saved View",
        "PM-VIEW-.####",
        "title",
        [
            ("title", "Title", "Data", None, "req,list"),
            ("reference_doctype", "DocType", "Link", "DocType", "req"),
            ("filters", "Filters (JSON)", "Code", "JSON"),
            ("shared", "Shared With Team", "Check"),
        ],
    ),
]
