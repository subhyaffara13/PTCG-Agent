
def get_bad_protocol_flags(
    left: Instance, right: Instance, class_obj: bool = False
) -> list[tuple[str, set[int], set[int]]]:
    """Return all incompatible attribute flags for members that are present in both
    'left' and 'right'.
    """
    assert right.type.is_protocol
    all_flags: list[tuple[str, set[int], set[int]]] = []
    for member in right.type.protocol_members:
        if find_member(member, left, left, class_obj=class_obj):
            all_flags.append(
                (
                    member,
                    get_member_flags(member, left, class_obj=class_obj),
                    get_member_flags(member, right),
                )
            )
    bad_flags = []
    for name, subflags, superflags in all_flags:
        if (
            IS_CLASSVAR in subflags
            and IS_CLASSVAR not in superflags
            and IS_SETTABLE in superflags
            or IS_CLASSVAR in superflags
            and IS_CLASSVAR not in subflags
            or IS_SETTABLE in superflags
            and IS_SETTABLE not in subflags
            or IS_CLASS_OR_STATIC in superflags
            and IS_CLASS_OR_STATIC not in subflags
            or class_obj
            and IS_VAR in superflags
            and IS_CLASSVAR not in subflags
            or class_obj
            and IS_CLASSVAR in superflags
        ):
            bad_flags.append((name, subflags, superflags))
    return bad_flags

