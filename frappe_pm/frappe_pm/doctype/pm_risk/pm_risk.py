from frappe.model.document import Document

LEVEL = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}


class PMRisk(Document):
    def validate(self):
        self.score = LEVEL.get(self.probability, 2) * LEVEL.get(self.impact, 2)
