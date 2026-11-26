"""Pure-Python graph helpers (no Frappe import, so they unit-test without a site)."""


def has_cycle(edges, start):
    """edges: {task: [deps]}; True if a path from start leads back to start."""
    seen, stack = set(), list(edges.get(start, []))
    while stack:
        cur = stack.pop()
        if cur == start:
            return True
        if cur in seen:
            continue
        seen.add(cur)
        stack.extend(edges.get(cur, []))
    return False
