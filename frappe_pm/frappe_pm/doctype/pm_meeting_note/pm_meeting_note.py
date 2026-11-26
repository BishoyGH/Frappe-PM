import frappe
from frappe.model.document import Document


class PMMeetingNote(Document):
    @frappe.whitelist()
    def create_tasks(self):
        """Turn action items into tasks on the meeting's project."""
        created = []
        for row in self.actions:
            if row.task:
                continue
            task = frappe.get_doc(
                {
                    "doctype": "PM Task",
                    "subject": row.action,
                    "project": self.project,
                    "due_date": row.due_date,
                }
            ).insert()
            if row.owner_user:
                from frappe.desk.form.assign_to import add

                add({"doctype": "PM Task", "name": task.name, "assign_to": [row.owner_user]})
            row.db_set("task", task.name)
            created.append(task.name)
        return created
