
def analyze_always_defined_attrs(class_irs: list[ClassIR]) -> None:
    """Find always defined attributes all classes of a compilation unit.

    Also tag attribute initialization ops to not decref the previous
    value (as this would read a NULL pointer and segfault).

    Update the _always_initialized_attrs, _sometimes_initialized_attrs
    and init_self_leak attributes in ClassIR instances.

    This is the main entry point.
    """
    seen: set[ClassIR] = set()

    # First pass: only look at target class and classes in MRO
    for cl in class_irs:
        analyze_always_defined_attrs_in_class(cl, seen)

    # Second pass: look at all derived class
    seen = set()
    for cl in class_irs:
        update_always_defined_attrs_using_subclasses(cl, seen)

    # Final pass: detect attributes that need to use a bitmap to track definedness
    seen = set()
    for cl in class_irs:
        detect_undefined_bitmap(cl, seen)

