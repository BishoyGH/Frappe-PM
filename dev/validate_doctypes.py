"""Static checks on generated DocTypes: valid JSON, link targets exist, table options are child tables."""

import glob
import json
import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
docs = {}
for p in glob.glob(os.path.join(root, "frappe_pm", "frappe_pm", "doctype", "*", "*.json")):
    d = json.load(open(p))
    docs[d["name"]] = d
STD = {
    "User",
    "Currency",
    "Holiday List",
    "Role",
    "Company",
    "Customer",
    "Employee",
    "Item",
    "Cost Center",
    "DocType",
}
errs = []
for name, d in docs.items():
    for f in d["fields"]:
        if f["fieldtype"] == "Link" and f.get("options") not in docs and f.get("options") not in STD:
            errs.append(f"{name}.{f['fieldname']}: unknown link target {f.get('options')}")
        if f["fieldtype"] in ("Table", "Table MultiSelect"):
            t = docs.get(f.get("options"))
            if not t or not t.get("istable"):
                errs.append(f"{name}.{f['fieldname']}: {f.get('options')} is not a child table")
    names = [f["fieldname"] for f in d["fields"]]
    if len(names) != len(set(names)):
        errs.append(f"{name}: duplicate fieldnames")
print(f"checked {len(docs)} doctypes")
if errs:
    print("\n".join(errs))
    sys.exit(1)

# standard documents must have valid JSON and the workspace may only reference existing doctypes

base = os.path.join(root, "frappe_pm", "frappe_pm")
for p in glob.glob(os.path.join(base, "*", "*", "*.json")):
    if "/doctype/" in p:
        continue
    json.load(open(p))
ws = json.load(open(os.path.join(base, "workspace", "frappe_pm", "frappe_pm.json")))
bad = [lk["link_to"] for lk in ws["links"] if lk.get("link_type") == "DocType" and lk["link_to"] not in docs]
if bad:
    print("workspace links to unknown doctypes:", bad)
    sys.exit(1)
print("standard documents OK")
