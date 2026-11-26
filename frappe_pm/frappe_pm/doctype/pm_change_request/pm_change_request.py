import frappe
from frappe import _
from frappe.model.document import Document


class PMChangeRequest(Document):
    def validate(self):
        if self.status == "Approved" and not frappe.has_permission("PM Change Request", "write"):
            frappe.throw(_("Not permitted to approve"))
