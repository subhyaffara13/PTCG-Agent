
def all_non_object_members(info: TypeInfo) -> set[str]:
    members = set(info.names)
    for base in info.mro[1:-1]:
        members.update(base.names)
    return members

