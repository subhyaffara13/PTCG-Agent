
def users():
    """Return currently connected users as a list of namedtuples."""
    retlist = []
    rawlist = cext.users()
    localhost = (':0.0', ':0')
    for item in rawlist:
        user, tty, hostname, tstamp, user_process, pid = item
        # note: the underlying C function includes entries about
        # system boot, run level and others.  We might want
        # to use them in the future.
        if not user_process:
            continue
        if hostname in localhost:
            hostname = 'localhost'
        nt = ntp.suser(user, tty, hostname, tstamp, pid)
        retlist.append(nt)
    return retlist


def users():
    """Return currently connected users as a list of namedtuples."""
    retlist = []
    rawlist = cext.users()
    for item in rawlist:
        user, tty, hostname, tstamp, pid = item
        if tty == '~':
            continue  # reboot or shutdown
        nt = ntp.suser(user, tty or None, hostname, tstamp, pid)
        retlist.append(nt)
    return retlist


def users():
    """Return currently connected users as a list of namedtuples."""
    retlist = []
    rawlist = cext.users()
    for item in rawlist:
        user, tty, hostname, tstamp, pid = item
        nt = ntp.suser(user, tty or None, hostname, tstamp, pid)
        retlist.append(nt)
    return retlist


def users():
    """Return currently connected users as a list of namedtuples."""
    retlist = []
    rawlist = cext.users()
    for item in rawlist:
        user, tty, hostname, tstamp, pid = item
        if tty == '~':
            continue  # reboot or shutdown
        if not tstamp:
            continue
        nt = ntp.suser(user, tty or None, hostname or None, tstamp, pid)
        retlist.append(nt)
    return retlist


def users():
    """Return currently connected users as a list of namedtuples."""
    retlist = []
    rawlist = cext.users()
    localhost = (':0.0', ':0')
    for item in rawlist:
        user, tty, hostname, tstamp, user_process, pid = item
        # note: the underlying C function includes entries about
        # system boot, run level and others.  We might want
        # to use them in the future.
        if not user_process:
            continue
        if hostname in localhost:
            hostname = 'localhost'
        nt = ntp.suser(user, tty, hostname, tstamp, pid)
        retlist.append(nt)
    return retlist


def users():
    """Return currently connected users as a list of namedtuples."""
    retlist = []
    rawlist = cext.users()
    for item in rawlist:
        user, hostname, tstamp = item
        nt = ntp.suser(user, None, hostname, tstamp, None)
        retlist.append(nt)
    return retlist


def users():
    """Return users currently connected on the system as a list of
    namedtuples including the following fields.

     - user: the name of the user
     - terminal: the tty or pseudo-tty associated with the user, if any.
     - host: the host name associated with the entry, if any.
     - started: the creation time as a floating point number expressed in
       seconds since the epoch.
    """
    return _psplatform.users()


def users():
    """Manage users on your LiteLLM proxy server"""
    pass

