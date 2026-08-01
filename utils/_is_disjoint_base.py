
def _is_disjoint_base(typ: type[object]) -> bool:
    """Return whether a type is a disjoint base at runtime, mirroring CPython's logic in typeobject.c.

    See PEP 800."""
    if typ is object:
        return True
    base = typ.__base__
    assert base is not None, f"Type {typ} has no base"
    return _shape_differs(typ, base)


def _is_disjoint_base(info: TypeInfo) -> bool:
    # It either has the @disjoint_base decorator or defines nonempty __slots__.
    if info.is_disjoint_base:
        return True
    if not info.slots:
        return False
    own_slots = {
        slot
        for slot in info.slots
        if not any(
            base_info.type.slots is not None and slot in base_info.type.slots
            for base_info in info.bases
        )
    }
    return bool(own_slots)

