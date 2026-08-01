
def can_have_shared_disjoint_base(instances: list[Instance]) -> bool:
    """Returns whether the given instances can share a disjoint base.

    This means that a child class of these classes can exist at runtime.
    """
    # Ignore None disjoint bases (which are `object`).
    disjoint_bases = [
        base for instance in instances if (base := _get_disjoint_base_of(instance)) is not None
    ]
    if not disjoint_bases:
        # All are `object`.
        return True

    candidate = disjoint_bases[0]
    for base in disjoint_bases[1:]:
        if candidate.has_base(base.fullname):
            continue
        elif base.has_base(candidate.fullname):
            candidate = base
        else:
            return False
    return True

