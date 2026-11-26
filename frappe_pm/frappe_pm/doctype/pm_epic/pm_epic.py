import frappe
from frappe.model.document import Document


class PMEpic(Document):
    def validate(self):
        if self.is_new():
            return
        r = frappe.db.sql(
            "select coalesce(avg(progress),0) from `tabPM Task` where epic=%s and status!='Cancelled'",
            self.name,
        )
        self.percent_complete = r[0][0]
