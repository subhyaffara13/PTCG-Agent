from typing import Set

def subset_elements(el: etree.Element, retained_ids: Set[str]) -> bool:
    # Keep elements if their id is in the subset, or any of their children's id is.
    # Drop elements whose id is not in the subset, and either have no children,
    # or all their children are being dropped.
    if el.attrib.get("id") in retained_ids:
        # if id is in the set, don't recurse; keep whole subtree
        return True
    # recursively subset all the children; we use a list comprehension instead
    # of a parentheses-less generator expression because we don't want any() to
    # short-circuit, as our function has a side effect of dropping empty elements.
    if any([subset_elements(e, retained_ids) for e in el]):
        return True
    assert len(el) == 0
    parent = el.getparent()
    if parent is not None:
        parent.remove(el)
    return False

