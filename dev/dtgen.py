"""Generate Frappe DocType JSON + controller stubs from compact specs in dev/specs/*.py.

Run: python dev/dtgen.py   (idempotent; never overwrites existing controllers)
"""

import glob
import importlib.util
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = "frappe_pm"
MODULE = "Frappe PM"
MOD_DIR = os.path.join(ROOT, APP, APP, "doctype")
TS = "2026-11-26 00:00:00.000000"


def snake(n):
    return re.sub(r"[^a-z0-9]+", "_", n.lower()).strip("_")


def pascal(n):
    return "".join(w.capitalize() for w in re.split(r"[^A-Za-z0-9]+", n) if w)


DEFAULT_ROLES = {
    "PM Admin": dict(create=1, delete=1, export=1, print=1, read=1, report=1, share=1, write=1, email=1),
    "Project Manager": dict(
        create=1, delete=1, export=1, print=1, read=1, report=1, share=1, write=1, email=1
    ),
    "Team Member": dict(create=1, read=1, report=1, write=1, print=1, email=1, share=1),
    "PM Viewer": dict(read=1, report=1, print=1),
}


def field(t):
    """t = (fieldname, label, fieldtype, options?, flags?) ; flags is a string like 'req,list,unique,ro,hidden,default=x,search,filter,hide_in_list'."""
    name, label, ftype = t[0], t[1], t[2]
    opts = t[3] if len(t) > 3 else None
    flags = (t[4] if len(t) > 4 else "") or ""
    f = {"fieldname": name, "fieldtype": ftype, "label": label}
    if opts:
        f["options"] = opts
    for fl in [x for x in flags.split(",") if x]:
        if fl == "req":
            f["reqd"] = 1
        elif fl == "list":
            f["in_list_view"] = 1
        elif fl == "unique":
            f["unique"] = 1
        elif fl == "ro":
            f["read_only"] = 1
        elif fl == "hidden":
            f["hidden"] = 1
        elif fl == "search":
            f["in_standard_filter"] = 1
        elif fl == "filter":
            f["in_standard_filter"] = 1
        elif fl == "preview":
            f["in_preview"] = 1
        elif fl == "bold":
            f["bold"] = 1
        elif fl == "idx":
            f["search_index"] = 1
        elif fl == "nocopy":
            f["no_copy"] = 1
        elif fl == "collapsible":
            f["collapsible"] = 1
        elif fl.startswith("default="):
            f["default"] = fl[8:]
        elif fl.startswith("dep="):
            f["depends_on"] = fl[4:]
        elif fl.startswith("fetch="):
            f["fetch_from"] = fl[6:]
        elif fl.startswith("desc="):
            f["description"] = fl[5:]
        elif fl.startswith("perm="):
            f["permlevel"] = int(fl[5:])
        else:
            raise ValueError(f"unknown flag {fl} in {name}")
    return f


def build(spec):
    name = spec["name"]
    fields = [field(t) for t in spec["fields"]]
    d = {
        "actions": [],
        "allow_rename": 1 if spec.get("rename") else 0,
        "creation": TS,
        "doctype": "DocType",
        "engine": "InnoDB",
        "field_order": [f["fieldname"] for f in fields],
        "fields": fields,
        "index_web_pages_for_search": 0,
        "links": spec.get("links", []),
        "modified": TS,
        "modified_by": "Administrator",
        "module": MODULE,
        "name": name,
        "owner": "Administrator",
        "permissions": [dict(role=r, **p) for r, p in (spec.get("perms") or DEFAULT_ROLES).items()],
        "sort_field": "modified",
        "sort_order": "DESC",
        "states": [],
    }
    d["permissions"].append(
        dict(
            role="System Manager",
            create=1,
            delete=1,
            read=1,
            report=1,
            share=1,
            write=1,
            export=1,
            print=1,
            email=1,
        )
    )
    if spec.get("autoname"):
        d["autoname"] = spec["autoname"]
    if spec.get("naming_rule"):
        d["naming_rule"] = spec["naming_rule"]
    if spec.get("table"):
        d["istable"] = 1
        d["editable_grid"] = 1
        d.pop("permissions", None)
    if spec.get("single"):
        d["issingle"] = 1
    if spec.get("submittable"):
        d["is_submittable"] = 1
    if spec.get("tree"):
        d["is_tree"] = 1
        d["nsm_parent_field"] = "parent_" + snake(name)
    if spec.get("title"):
        d["title_field"] = spec["title"]
        d["show_title_field_in_link"] = 1
    if spec.get("search"):
        d["search_fields"] = spec["search"]
    if spec.get("image"):
        d["image_field"] = spec["image"]
    if spec.get("track", not spec.get("table") and not spec.get("single")):
        d["track_changes"] = 1
    if spec.get("comments", True) and not spec.get("table") and not spec.get("single"):
        d["allow_import"] = 1
    if spec.get("quick"):
        d["quick_entry"] = 1
    if spec.get("desc"):
        d["description"] = spec["desc"]
    if spec.get("calendar") or spec.get("kanban"):
        pass
    return d


def write(spec):
    s = snake(spec["name"])
    path = os.path.join(MOD_DIR, s)
    os.makedirs(path, exist_ok=True)
    open(os.path.join(path, "__init__.py"), "a").close()
    with open(os.path.join(path, s + ".json"), "w") as fh:
        json.dump(build(spec), fh, indent=1, sort_keys=False)
        fh.write("\n")
    py = os.path.join(path, s + ".py")
    if not os.path.exists(py):
        base = "NestedSet" if spec.get("tree") else "Document"
        imp = (
            "from frappe.utils.nestedset import NestedSet"
            if spec.get("tree")
            else "from frappe.model.document import Document"
        )
        open(py, "w").write(f"{imp}\n\n\nclass {pascal(spec['name'])}({base}):\n    pass\n")
    return s


def main():
    specs = []
    for p in sorted(glob.glob(os.path.join(ROOT, "dev", "specs", "*.py"))):
        sp = importlib.util.spec_from_file_location("m", p)
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        specs += m.SPECS
    names = [s["name"] for s in specs]
    assert len(names) == len(set(names)), "duplicate doctype names"
    for s in specs:
        write(s)
    print(f"generated {len(specs)} DocTypes")


if __name__ == "__main__":
    main()
