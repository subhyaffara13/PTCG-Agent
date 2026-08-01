
def conn_to_ntuple(fd, fam, type_, laddr, raddr, status, status_map, pid=None):
    """Convert a raw connection tuple to a proper ntuple."""
    from . import _ntuples as ntp

    if fam in {socket.AF_INET, AF_INET6}:
        if laddr:
            laddr = ntp.addr(*laddr)
        if raddr:
            raddr = ntp.addr(*raddr)
    if type_ == socket.SOCK_STREAM and fam in {AF_INET, AF_INET6}:
        status = status_map.get(status, CONN_NONE)
    else:
        status = CONN_NONE  # ignore whatever C returned to us
    fam = sockfam_to_enum(fam)
    type_ = socktype_to_enum(type_)
    if pid is None:
        return ntp.pconn(fd, fam, type_, laddr, raddr, status)
    else:
        return ntp.sconn(fd, fam, type_, laddr, raddr, status, pid)

