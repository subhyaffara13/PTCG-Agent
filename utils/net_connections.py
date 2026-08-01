
def net_connections(kind, _pid=-1):
    """Return socket connections.  If pid == -1 return system-wide
    connections (as opposed to connections opened by one process only).
    """
    families, types = _common.conn_tmap[kind]
    rawlist = cext.net_connections(_pid)
    ret = []
    for item in rawlist:
        fd, fam, type_, laddr, raddr, status, pid = item
        if fam not in families:
            continue
        if type_ not in types:
            continue
        nt = conn_to_ntuple(
            fd,
            fam,
            type_,
            laddr,
            raddr,
            status,
            TCP_STATUSES,
            pid=pid if _pid == -1 else None,
        )
        ret.append(nt)
    return ret


def net_connections(kind):
    """System-wide network connections."""
    families, types = conn_tmap[kind]
    ret = set()
    if OPENBSD:
        rawlist = cext.net_connections(-1, families, types)
    elif NETBSD:
        rawlist = cext.net_connections(-1, kind)
    else:  # FreeBSD
        rawlist = cext.net_connections(families, types)

    for item in rawlist:
        fd, fam, type, laddr, raddr, status, pid = item
        nt = conn_to_ntuple(
            fd, fam, type, laddr, raddr, status, TCP_STATUSES, pid
        )
        ret.add(nt)
    return list(ret)


def net_connections(kind='inet'):
    """Return system-wide open connections."""
    return _net_connections.retrieve(kind)


def net_connections(kind='inet'):
    """System-wide network connections."""
    # Note: on macOS this will fail with AccessDenied unless
    # the process is owned by root.
    ret = []
    for pid in pids():
        try:
            cons = Process(pid).net_connections(kind)
        except NoSuchProcess:
            continue
        else:
            if cons:
                for c in cons:
                    c = list(c) + [pid]
                    ret.append(ntp.sconn(*c))
    return ret


def net_connections(kind, _pid=-1):
    """Return socket connections.  If pid == -1 return system-wide
    connections (as opposed to connections opened by one process only).
    Only INET sockets are returned (UNIX are not).
    """
    families, types = _common.conn_tmap[kind]
    rawlist = cext.net_connections(_pid)
    ret = set()
    for item in rawlist:
        fd, fam, type_, laddr, raddr, status, pid = item
        if fam not in families:
            continue
        if type_ not in types:
            continue
        # TODO: refactor and use _common.conn_to_ntuple.
        if fam in {AF_INET, AF_INET6}:
            if laddr:
                laddr = ntp.addr(*laddr)
            if raddr:
                raddr = ntp.addr(*raddr)
        status = TCP_STATUSES[status]
        fam = sockfam_to_enum(fam)
        type_ = socktype_to_enum(type_)
        if _pid == -1:
            nt = ntp.sconn(fd, fam, type_, laddr, raddr, status, pid)
        else:
            nt = ntp.pconn(fd, fam, type_, laddr, raddr, status)
        ret.add(nt)
    return list(ret)


def net_connections(kind, _pid=-1):
    """Return socket connections.  If pid == -1 return system-wide
    connections (as opposed to connections opened by one process only).
    """
    families, types = conn_tmap[kind]
    rawlist = cext.net_connections(_pid, families, types)
    ret = set()
    for item in rawlist:
        fd, fam, type, laddr, raddr, status, pid = item
        nt = conn_to_ntuple(
            fd,
            fam,
            type,
            laddr,
            raddr,
            status,
            TCP_STATUSES,
            pid=pid if _pid == -1 else None,
        )
        ret.add(nt)
    return list(ret)


def net_connections(kind='inet'):
    """Return system-wide socket connections as a list of
    (fd, family, type, laddr, raddr, status, pid) namedtuples.
    In case of limited privileges 'fd' and 'pid' may be set to -1
    and None respectively.
    The *kind* parameter filters for connections that fit the
    following criteria:

    +------------+----------------------------------------------------+
    | Kind Value | Connections using                                  |
    +------------+----------------------------------------------------+
    | inet       | IPv4 and IPv6                                      |
    | inet4      | IPv4                                               |
    | inet6      | IPv6                                               |
    | tcp        | TCP                                                |
    | tcp4       | TCP over IPv4                                      |
    | tcp6       | TCP over IPv6                                      |
    | udp        | UDP                                                |
    | udp4       | UDP over IPv4                                      |
    | udp6       | UDP over IPv6                                      |
    | unix       | UNIX socket (both UDP and TCP protocols)           |
    | all        | the sum of all the possible families and protocols |
    +------------+----------------------------------------------------+

    On macOS this function requires root privileges.
    """
    _check_conn_kind(kind)
    return _psplatform.net_connections(kind)

