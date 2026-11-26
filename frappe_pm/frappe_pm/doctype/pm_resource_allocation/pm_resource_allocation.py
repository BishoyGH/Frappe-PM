import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate


class PMResourceAllocation(Document):
    def validate(self):
        if getdate(self.end_date) < getdate(self.start_date):
            frappe.throw(_("End Date cannot be before Start Date"))
        cap = frappe.db.get_value("PM Resource Profile", self.user, "weekly_capacity_hours") or 40
        self.hours_per_week = cap * (self.allocation_percent or 0) / 100
        total = self.total_allocation()
        if total > 100:
            frappe.msgprint(
                _("{0} is allocated {1}% over this period (over-allocated)").format(self.user, total),
                indicator="orange",
                alert=True,
            )

    def total_allocation(self):
        rows = frappe.db.sql(
            """select coalesce(sum(allocation_percent), 0) from `tabPM Resource Allocation`
            where user = %s and name != %s and start_date <= %s and end_date >= %s""",
            (self.user, self.name or "", self.end_date, self.start_date),
        )
        return (rows[0][0] or 0) + (self.allocation_percent or 0)
