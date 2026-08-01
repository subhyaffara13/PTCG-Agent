
def disk_usage(path):
    """Return disk usage associated with path.
    Note: UNIX usually reserves 5% disk space which is not accessible
    by user. In this function "total" and "used" values reflect the
    total and used disk space whereas "free" and "percent" represent
    the "free" and "used percent" user disk space.
    """
    st = os.statvfs(path)
    # Total space which is only available to root (unless changed
    # at system level).
    total = st.f_blocks * st.f_frsize
    # Remaining free space usable by root.
    avail_to_root = st.f_bfree * st.f_frsize
    # Remaining free space usable by user.
    avail_to_user = st.f_bavail * st.f_frsize
    # Total space being used in general.
    used = total - avail_to_root
    if MACOS:
        # see: https://github.com/giampaolo/psutil/pull/2152
        used = _psutil_osx.disk_usage_used(path, used)
    # Total space which is available to user (same as 'total' but
    # for the user).
    total_user = used + avail_to_user
    # User usage percent compared to the total amount of space
    # the user can use. This number would be higher if compared
    # to root's because the user has less space (usually -5%).
    usage_percent_user = usage_percent(used, total_user, round_=1)

    # NB: the percentage is -5% than what shown by df due to
    # reserved blocks that we are currently not considering:
    # https://github.com/giampaolo/psutil/issues/829#issuecomment-223750462
    return ntp.sdiskusage(
        total=total, used=used, free=avail_to_user, percent=usage_percent_user
    )


def disk_usage(path):
    """Return disk usage associated with path."""
    if isinstance(path, bytes):
        # XXX: do we want to use "strict"? Probably yes, in order
        # to fail immediately. After all we are accepting input here...
        path = path.decode(ENCODING, errors="strict")
    total, used, free = cext.disk_usage(path)
    percent = usage_percent(used, total, round_=1)
    return ntp.sdiskusage(total, used, free, percent)


def disk_usage(path):
    """Return disk usage statistics about the given *path* as a
    namedtuple including total, used and free space expressed in bytes
    plus the percentage usage.
    """
    return _psplatform.disk_usage(path)

