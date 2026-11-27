import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_days, nowdate


def make_project(**kw):
    return frappe.get_doc(
        {"doctype": "PM Project", "project_name": kw.pop("project_name", "Test Project"), **kw}
    ).insert()


def make_task(project, **kw):
    return frappe.get_doc(
        {"doctype": "PM Task", "subject": kw.pop("subject", "Test Task"), "project": project, **kw}
    ).insert()


class TestProject(FrappeTestCase):
    def test_dates_validated(self):
        with self.assertRaises(frappe.ValidationError):
            make_project(start_date=nowdate(), end_date=add_days(nowdate(), -1))

    def test_rollup(self):
        p = make_project()
        t1 = make_task(p.name)
        make_task(p.name, subject="Two")
        t1.status = "Completed"
        t1.save()
        p.reload()
        self.assertEqual((p.total_tasks, p.completed_tasks), (2, 1))
        self.assertEqual(p.percent_complete, 50)

    def test_duplicate_member(self):
        with self.assertRaises(frappe.ValidationError):
            make_project(members=[{"user": "Administrator"}, {"user": "Administrator"}])


class TestTask(FrappeTestCase):
    def test_due_before_start(self):
        p = make_project()
        with self.assertRaises(frappe.ValidationError):
            make_task(p.name, start_date=nowdate(), due_date=add_days(nowdate(), -2))

    def test_overdue_flag(self):
        p = make_project()
        t = make_task(p.name, due_date=add_days(nowdate(), -3))
        self.assertEqual(t.is_overdue, 1)

    def test_dependency_cycle(self):
        p = make_project()
        a, b = make_task(p.name, subject="A"), make_task(p.name, subject="B")
        b.append("depends_on", {"depends_on_task": a.name})
        b.save()
        a.append("depends_on", {"depends_on_task": b.name})
        with self.assertRaises(frappe.ValidationError):
            a.save()

    def test_parent_same_project(self):
        p1, p2 = make_project(), make_project(project_name="Other")
        parent = make_task(p1.name, is_group=1)
        with self.assertRaises(frappe.ValidationError):
            make_task(p2.name, parent_pm_task=parent.name)

    def test_recurring_spawns_next(self):
        p = make_project()
        t = make_task(p.name, is_recurring=1, recurrence="Weekly", due_date=nowdate())
        t.status = "Completed"
        t.save()
        self.assertEqual(frappe.db.count("PM Task", {"project": p.name}), 2)


class TestTimesheet(FrappeTestCase):
    def _sheet(self, logs):
        p = make_project()
        return frappe.get_doc(
            {
                "doctype": "PM Timesheet",
                "user": "Administrator",
                "time_logs": [{"project": p.name, **log} for log in logs],
            }
        )

    def test_hours_calculated(self):
        ts = self._sheet(
            [{"from_time": "2026-01-05 09:00:00", "to_time": "2026-01-05 11:30:00", "billable": 1}]
        ).insert()
        self.assertEqual(ts.total_hours, 2.5)

    def test_overlap_rejected(self):
        with self.assertRaises(frappe.ValidationError):
            self._sheet(
                [
                    {"from_time": "2026-01-05 09:00:00", "to_time": "2026-01-05 11:00:00"},
                    {"from_time": "2026-01-05 10:00:00", "to_time": "2026-01-05 12:00:00"},
                ]
            ).insert()


class TestSprint(FrappeTestCase):
    def test_single_active_sprint(self):
        p = make_project()
        mk = lambda n, s: frappe.get_doc(
            {
                "doctype": "PM Sprint",
                "sprint_name": n,
                "project": p.name,
                "status": s,
                "start_date": nowdate(),
                "end_date": add_days(nowdate(), 14),
            }
        ).insert()
        mk("S1", "Active")
        with self.assertRaises(frappe.ValidationError):
            mk("S2", "Active")


class TestExtended(FrappeTestCase):
    def test_risk_score(self):
        p = make_project()
        r = frappe.get_doc(
            {
                "doctype": "PM Risk",
                "title": "R",
                "project": p.name,
                "probability": "High",
                "impact": "Critical",
            }
        ).insert()
        self.assertEqual(r.score, 12)

    def test_budget_totals(self):
        p = make_project()
        b = frappe.get_doc(
            {
                "doctype": "PM Project Budget",
                "project": p.name,
                "lines": [{"category": "Labor", "planned_amount": 100, "actual_amount": 30}],
            }
        ).insert()
        self.assertEqual(b.variance, 70)

    def test_reports_run(self):
        from frappe_pm.frappe_pm.report.pm_overdue_tasks.pm_overdue_tasks import execute

        cols, rows = execute({})
        self.assertTrue(cols)


class TestApi(FrappeTestCase):
    def test_bulk_update_rejects_unknown_field(self):
        from frappe_pm.api import bulk_update_tasks

        with self.assertRaises(frappe.ValidationError):
            bulk_update_tasks("[]", '{"owner": "x"}')

    def test_overview(self):
        from frappe_pm.api import project_overview

        p = make_project()
        make_task(p.name)
        self.assertEqual(project_overview(p.name)["project"], p.name)
