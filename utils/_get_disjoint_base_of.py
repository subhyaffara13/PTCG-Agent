
def _get_disjoint_base_of(instance: Instance) -> TypeInfo | None:
    """Returns the disjoint base of the given instance, if it exists."""
    if _is_disjoint_base(instance.type):
        return instance.type
    for base in instance.type.mro:
        if _is_disjoint_base(base):
            return base
    return None

