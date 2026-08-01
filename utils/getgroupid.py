
def getgroupid(group):
    import grp

    if not isinstance(group, int):
        group = grp.getgrnam(group)[2]  # type:ignore[attr-defined,unused-ignore]
    return group

