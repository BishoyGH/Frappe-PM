from frappe.model.document import Document
from frappe.utils import nowdate


class PMMilestone(Document):
    def validate(self):
        self.completed_on = (self.completed_on or nowdate()) if self.status == "Completed" else None
