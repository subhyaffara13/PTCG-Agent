
def update_always_defined_attrs_using_subclasses(cl: ClassIR, seen: set[ClassIR]) -> None:
    """Remove attributes not defined in all subclasses from always defined attrs."""
    if cl in seen:
        return
    if cl.children is None:
        # Subclasses are unknown
        return
    removed = set()
    for attr in cl._always_initialized_attrs:
        for child in cl.children:
            update_always_defined_attrs_using_subclasses(child, seen)
            if attr not in child._always_initialized_attrs:
                removed.add(attr)
    cl._always_initialized_attrs -= removed
    seen.add(cl)

