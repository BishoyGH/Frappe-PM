import json

import frappe
from frappe.model.document import Document


class PMBaseline(Document):
    def before_insert(self):
        tasks = frappe.get_all(
            "PM Task",
            filters={"project": self.project},
            fields=["name", "subject", "start_date", "due_date", "estimated_hours", "status"],
        )
        self.snapshot = json.dumps(tasks, default=str)
