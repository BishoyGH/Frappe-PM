import unittest

from frappe_pm.graph import has_cycle


class TestCycle(unittest.TestCase):
    def test_no_cycle(self):
        self.assertFalse(has_cycle({"a": ["b"], "b": ["c"]}, "a"))

    def test_cycle(self):
        self.assertTrue(has_cycle({"a": ["b"], "b": ["c"], "c": ["a"]}, "a"))

    def test_self_loop(self):
        self.assertTrue(has_cycle({"a": ["a"]}, "a"))
