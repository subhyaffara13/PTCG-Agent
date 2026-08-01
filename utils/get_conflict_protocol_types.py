
def get_conflict_protocol_types(
    left: Instance,
    original_left: Type,
    right: Instance,
    class_obj: bool = False,
    options: Options | None = None,
) -> list[tuple[str, Type, Type, bool]]:
    """Find members that are defined in 'left' but have incompatible types.
    Return them as a list of ('member', 'got', 'expected', 'is_lvalue').
    """
    assert right.type.is_protocol
    conflicts: list[tuple[str, Type, Type, bool]] = []
    for member in right.type.protocol_members:
        if member in ("__init__", "__new__"):
            continue
        supertype = find_member(member, right, left)
        assert supertype is not None
        subtype = get_protocol_member(left, original_left, member, class_obj)
        if not subtype:
            continue
        is_compat = is_subtype(subtype, supertype, ignore_pos_arg_names=True, options=options)
        if not is_compat:
            conflicts.append((member, subtype, supertype, False))
        superflags = get_member_flags(member, right)
        if IS_SETTABLE not in superflags:
            continue
        different_setter = False
        if IS_EXPLICIT_SETTER in superflags:
            set_supertype = find_member(member, right, left, is_lvalue=True)
            if set_supertype and not is_same_type(set_supertype, supertype):
                different_setter = True
            supertype = set_supertype
        if IS_EXPLICIT_SETTER in get_member_flags(member, left):
            set_subtype = get_protocol_member(
                left, original_left, member, class_obj, is_lvalue=True
            )
            if set_subtype and not is_same_type(set_subtype, subtype):
                different_setter = True
            subtype = set_subtype
        if not is_compat and not different_setter:
            # We already have this conflict listed, avoid duplicates.
            continue
        assert supertype is not None and subtype is not None
        is_compat = is_subtype(supertype, subtype, options=options)
        if not is_compat:
            conflicts.append((member, subtype, supertype, different_setter))
    return conflicts

