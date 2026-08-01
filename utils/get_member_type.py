
def get_member_type(cls: Any, member_name: str) -> MemberType | None:
    """
    Get the MemberType for a specific member of an opaque object class.

    Args:
        cls: The opaque object class (or its string name)
        member_name: The name of the member to query

    Returns:
        MemberType if the member is registered, None otherwise
    """
    info = get_opaque_obj_info(cls)
    if info is None:
        return None
    return info.members.get(member_name)

