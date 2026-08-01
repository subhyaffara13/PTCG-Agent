
def get_missing_protocol_members(left: Instance, right: Instance, skip: list[str]) -> list[str]:
    """Find all protocol members of 'right' that are not implemented
    (i.e. completely missing) in 'left'.
    """
    assert right.type.is_protocol
    missing: list[str] = []
    for member in right.type.protocol_members:
        if member in skip:
            continue
        if not find_member(member, left, left):
            missing.append(member)
    return missing

