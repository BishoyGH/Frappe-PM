import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, get_datetime, getdate, nowdate, time_diff_in_hours


class PMTimesheet(Document):
    def validate(self):
        self.validate_lock()
        self.calculate()
        self.validate_overlap()

    def validate_lock(self):
        days = frappe.db.get_single_value("PM Settings", "lock_timesheets_after_days") or 0
        if days and self.start_date and getdate(self.start_date) < getdate(add_days(nowdate(), -days)):
            frappe.throw(_("Timesheets older than {0} days are locked").format(days))

    def calculate(self):
        total = billable = amount = cost = 0.0
        for row in self.time_logs:
            if row.from_time and row.to_time:
                if get_datetime(row.to_time) <= get_datetime(row.from_time):
                    frappe.throw(_("Row {0}: To time must be after From time").format(row.idx))
                row.hours = round(time_diff_in_hours(row.to_time, row.from_time), 4)
            if (row.hours or 0) <= 0:
                frappe.throw(_("Row {0}: Hours must be greater than zero").format(row.idx))
            if row.activity_type and not row.billing_rate:
                at = frappe.db.get_value(
                    "PM Activity Type",
                    row.activity_type,
                    ["billing_rate", "costing_rate", "billable"],
                    as_dict=True,
                )
                if at:
                    row.billing_rate = at.billing_rate
                    row.costing_rate = row.costing_rate or at.costing_rate
            total += row.hours
            if row.billable:
                billable += row.hours
                amount += row.hours * (row.billing_rate or 0)
            cost += row.hours * (row.costing_rate or 0)
        self.total_hours = total
        self.total_billable_hours = billable
        self.total_billable_amount = amount
        self.total_costing_amount = cost
        dates = [getdate(r.from_time) for r in self.time_logs if r.from_time]
        if dates:
            self.start_date = min(dates)
            self.end_date = max(dates)

    def validate_overlap(self):
        if frappe.db.get_single_value("PM Settings", "allow_overlapping_time"):
            return
        logs = sorted(
            (r for r in self.time_logs if r.from_time and r.to_time), key=lambda r: get_datetime(r.from_time)
        )
        for a, b in zip(logs, logs[1:]):
            if get_datetime(b.from_time) < get_datetime(a.to_time):
                frappe.throw(_("Time logs in rows {0} and {1} overlap").format(a.idx, b.idx))
        if not logs:
            return
        lo, hi = get_datetime(logs[0].from_time), get_datetime(logs[-1].to_time)
        clash = frappe.db.sql(
            """select ts.name from `tabPM Timesheet` ts join `tabPM Time Log` tl on tl.parent = ts.name
			where ts.user = %s and ts.docstatus = 1 and ts.name != %s and tl.from_time < %s and tl.to_time > %s limit 1""",
            (self.user, self.name or "", hi, lo),
        )
        if clash:
            frappe.throw(_("Time overlaps with submitted timesheet {0}").format(clash[0][0]))

    def on_submit(self):
        self.db_set("status", "Submitted")
        self.update_task_hours()

    def on_cancel(self):
        self.db_set("status", "Cancelled")
        self.update_task_hours()

    def update_task_hours(self):
        for task in {r.task for r in self.time_logs if r.task}:
            total = frappe.db.sql(
                """select coalesce(sum(tl.hours),0) from `tabPM Time Log` tl join `tabPM Timesheet` ts on ts.name = tl.parent
				where ts.docstatus = 1 and tl.task = %s""",
                task,
            )[0][0]
            frappe.db.set_value("PM Task", task, "actual_hours", total, update_modified=False)
        for project in {r.project for r in self.time_logs if r.project}:
            cost = frappe.db.sql(
                """select coalesce(sum(tl.hours * tl.costing_rate),0) from `tabPM Time Log` tl join `tabPM Timesheet` ts on ts.name = tl.parent
				where ts.docstatus = 1 and tl.project = %s""",
                project,
            )[0][0]
            frappe.db.set_value("PM Project", project, "actual_cost", cost, update_modified=False)
