import re
import subprocess
import sys

def net_if_stats():
    """Get NIC stats (isup, duplex, speed, mtu)."""
    duplex_map = {"Full": NIC_DUPLEX_FULL, "Half": NIC_DUPLEX_HALF}
    names = {x[0] for x in net_if_addrs()}
    ret = {}
    for name in names:
        mtu = cext.net_if_mtu(name)
        flags = cext.net_if_flags(name)

        # try to get speed and duplex
        # TODO: rewrite this in C (entstat forks, so use truss -f to follow.
        # looks like it is using an undocumented ioctl?)
        duplex = ""
        speed = 0
        p = subprocess.Popen(
            ["/usr/bin/entstat", "-d", name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = p.communicate()
        stdout, stderr = (
            x.decode(sys.stdout.encoding) for x in (stdout, stderr)
        )
        if p.returncode == 0:
            re_result = re.search(
                r"Running: (\d+) Mbps.*?(\w+) Duplex", stdout
            )
            if re_result is not None:
                speed = int(re_result.group(1))
                duplex = re_result.group(2)

        output_flags = ','.join(flags)
        isup = 'running' in flags
        duplex = duplex_map.get(duplex, NIC_DUPLEX_UNKNOWN)
        ret[name] = ntp.snicstats(isup, duplex, speed, mtu, output_flags)
    return ret


def net_if_stats():
    """Get NIC stats (isup, duplex, speed, mtu)."""
    names = net_io_counters().keys()
    ret = {}
    for name in names:
        try:
            mtu = cext.net_if_mtu(name)
            flags = cext.net_if_flags(name)
            duplex, speed = cext.net_if_duplex_speed(name)
        except OSError as err:
            # https://github.com/giampaolo/psutil/issues/1279
            if err.errno != errno.ENODEV:
                raise
        else:
            if hasattr(_common, 'NicDuplex'):
                duplex = _common.NicDuplex(duplex)
            output_flags = ','.join(flags)
            isup = 'running' in flags
            ret[name] = ntp.snicstats(isup, duplex, speed, mtu, output_flags)
    return ret


def net_if_stats():
    """Get NIC stats (isup, duplex, speed, mtu)."""
    duplex_map = {
        cext.DUPLEX_FULL: NIC_DUPLEX_FULL,
        cext.DUPLEX_HALF: NIC_DUPLEX_HALF,
        cext.DUPLEX_UNKNOWN: NIC_DUPLEX_UNKNOWN,
    }
    names = net_io_counters().keys()
    ret = {}
    for name in names:
        try:
            mtu = cext.net_if_mtu(name)
            flags = cext.net_if_flags(name)
            duplex, speed = cext.net_if_duplex_speed(name)
        except OSError as err:
            # https://github.com/giampaolo/psutil/issues/1279
            if err.errno != errno.ENODEV:
                raise
            debug(err)
        else:
            output_flags = ','.join(flags)
            isup = 'running' in flags
            ret[name] = ntp.snicstats(
                isup, duplex_map[duplex], speed, mtu, output_flags
            )
    return ret


def net_if_stats():
    """Get NIC stats (isup, duplex, speed, mtu)."""
    names = net_io_counters().keys()
    ret = {}
    for name in names:
        try:
            mtu = cext.net_if_mtu(name)
            flags = cext.net_if_flags(name)
            duplex, speed = cext.net_if_duplex_speed(name)
        except OSError as err:
            # https://github.com/giampaolo/psutil/issues/1279
            if err.errno != errno.ENODEV:
                raise
        else:
            if hasattr(_common, 'NicDuplex'):
                duplex = _common.NicDuplex(duplex)
            output_flags = ','.join(flags)
            isup = 'running' in flags
            ret[name] = ntp.snicstats(isup, duplex, speed, mtu, output_flags)
    return ret


def net_if_stats():
    """Get NIC stats (isup, duplex, speed, mtu)."""
    ret = cext.net_if_stats()
    for name, items in ret.items():
        isup, duplex, speed, mtu = items
        if hasattr(_common, 'NicDuplex'):
            duplex = _common.NicDuplex(duplex)
        ret[name] = ntp.snicstats(isup, duplex, speed, mtu, '')
    return ret


def net_if_stats():
    """Get NIC stats (isup, duplex, speed, mtu)."""
    ret = {}
    rawdict = cext.net_if_stats()
    for name, items in rawdict.items():
        isup, duplex, speed, mtu = items
        if hasattr(_common, 'NicDuplex'):
            duplex = _common.NicDuplex(duplex)
        ret[name] = ntp.snicstats(isup, duplex, speed, mtu, '')
    return ret


def net_if_stats():
    """Return information about each NIC (network interface card)
    installed on the system as a dictionary whose keys are the
    NIC names and value is a namedtuple with the following fields:

     - isup: whether the interface is up (bool)
     - duplex: can be either NIC_DUPLEX_FULL, NIC_DUPLEX_HALF or
               NIC_DUPLEX_UNKNOWN
     - speed: the NIC speed expressed in mega bits (MB); if it can't
              be determined (e.g. 'localhost') it will be set to 0.
     - mtu: the maximum transmission unit expressed in bytes.
    """
    return _psplatform.net_if_stats()

