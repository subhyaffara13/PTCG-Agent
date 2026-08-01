
def net_if_addrs():
    """Return the addresses associated to each NIC."""
    return cext.net_if_addrs()


def net_if_addrs():
    """Return the addresses associated to each NIC (network interface
    card) installed on the system as a dictionary whose keys are the
    NIC names and value is a list of namedtuples for each address
    assigned to the NIC. Each namedtuple includes 5 fields:

     - family: can be either socket.AF_INET, socket.AF_INET6 or
               psutil.AF_LINK, which refers to a MAC address.
     - address: is the primary address and it is always set.
     - netmask: and 'broadcast' and 'ptp' may be None.
     - ptp: stands for "point to point" and references the
            destination address on a point to point interface
            (typically a VPN).
     - broadcast: and *ptp* are mutually exclusive.

    Note: you can have more than one address of the same family
    associated with each interface.
    """
    rawlist = _psplatform.net_if_addrs()
    rawlist.sort(key=lambda x: x[1])  # sort by family
    ret = collections.defaultdict(list)
    for name, fam, addr, mask, broadcast, ptp in rawlist:
        try:
            fam = socket.AddressFamily(fam)
        except ValueError:
            if WINDOWS and fam == -1:
                fam = _psplatform.AF_LINK
            elif (
                hasattr(_psplatform, "AF_LINK") and fam == _psplatform.AF_LINK
            ):
                # Linux defines AF_LINK as an alias for AF_PACKET.
                # We re-set the family here so that repr(family)
                # will show AF_LINK rather than AF_PACKET
                fam = _psplatform.AF_LINK

        if fam == _psplatform.AF_LINK:
            # The underlying C function may return an incomplete MAC
            # address in which case we fill it with null bytes, see:
            # https://github.com/giampaolo/psutil/issues/786
            separator = ":" if POSIX else "-"
            while addr.count(separator) < 5:
                addr += f"{separator}00"

        nt = _ntp.snicaddr(fam, addr, mask, broadcast, ptp)

        # On Windows broadcast is None, so we determine it via
        # ipaddress module.
        if WINDOWS and fam in {socket.AF_INET, socket.AF_INET6}:
            try:
                broadcast = _common.broadcast_addr(nt)
            except Exception as err:  # noqa: BLE001
                debug(err)
            else:
                if broadcast is not None:
                    nt._replace(broadcast=broadcast)

        ret[name].append(nt)

    return dict(ret)

