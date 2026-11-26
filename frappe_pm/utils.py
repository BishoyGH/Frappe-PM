import frappe
from frappe.utils import add_days, getdate

_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def working_days():
    raw = frappe.db.get_single_value("PM Settings", "working_days") or "Mon Tue Wed Thu Fri"
    return {d for d in raw.replace(",", " ").split() if d in _DAYS}


def is_working_day(date, days=None):
    days = days or working_days()
    return _DAYS[getdate(date).weekday()] in days


def add_working_days(date, n):
    """Add n working days (n may be negative); n == 0 returns date unchanged."""
    days = working_days()
    d = getdate(date)
    step = 1 if n >= 0 else -1
    remaining = abs(n)
    while remaining:
        d = add_days(d, step)
        if is_working_day(d, days):
            remaining -= 1
    return d
