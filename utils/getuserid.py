
def getuserid(user):
    import pwd

    if not isinstance(user, int):
        user = pwd.getpwnam(user)[2]  # type:ignore[attr-defined,unused-ignore]
    return user

