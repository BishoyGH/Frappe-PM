import frappe
from frappe import _
from frappe.model.document import Document


class PMProjectBudget(Document):
    def validate(self):
        self.total_planned = sum(r.planned_amount or 0 for r in self.lines)
        self.total_actual = sum(r.actual_amount or 0 for r in self.lines)
        self.variance = self.total_planned - self.total_actual
        pct = self.alert_threshold_percent or 90
        if self.total_planned and self.total_actual >= self.total_planned * pct / 100:
            frappe.msgprint(
                _("Spend has reached {0}% of the planned budget").format(pct), indicator="orange", alert=True
            )

    def on_update(self):
        if self.status == "Approved":
            frappe.db.set_value(
                "PM Project", self.project, "budget", self.total_planned, update_modified=False
            )
