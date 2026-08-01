
def net_io_counters():
    """Return network I/O statistics for every network interface
    installed on the system as a dict of raw tuples.
    """
    with open_text(f"{get_procfs_path()}/net/dev") as f:
        lines = f.readlines()
    retdict = {}
    for line in lines[2:]:
        colon = line.rfind(':')
        assert colon > 0, repr(line)
        name = line[:colon].strip()
        fields = line[colon + 1 :].strip().split()

        (
            # in
            bytes_recv,
            packets_recv,
            errin,
            dropin,
            _fifoin,  # unused
            _framein,  # unused
            _compressedin,  # unused
            _multicastin,  # unused
            # out
            bytes_sent,
            packets_sent,
            errout,
            dropout,
            _fifoout,  # unused
            _collisionsout,  # unused
            _carrierout,  # unused
            _compressedout,  # unused
        ) = map(int, fields)

        retdict[name] = (
            bytes_sent,
            bytes_recv,
            packets_sent,
            packets_recv,
            errin,
            errout,
            dropin,
            dropout,
        )
    return retdict


def net_io_counters():
    """Return network I/O statistics for every network interface
    installed on the system as a dict of raw tuples.
    """
    return cext.net_io_counters()


def net_io_counters(pernic=False, nowrap=True):
    """Return network I/O statistics as a namedtuple including
    the following fields:

     - bytes_sent:   number of bytes sent
     - bytes_recv:   number of bytes received
     - packets_sent: number of packets sent
     - packets_recv: number of packets received
     - errin:        total number of errors while receiving
     - errout:       total number of errors while sending
     - dropin:       total number of incoming packets which were dropped
     - dropout:      total number of outgoing packets which were dropped
                     (always 0 on macOS and BSD)

    If *pernic* is True return the same information for every
    network interface installed on the system as a dictionary
    with network interface names as the keys and the namedtuple
    described above as the values.

    If *nowrap* is True it detects and adjust the numbers which overflow
    and wrap (restart from 0) and add "old value" to "new value" so that
    the returned numbers will always be increasing or remain the same,
    but never decrease.
    "net_io_counters.cache_clear()" can be used to invalidate the
    cache.
    """
    rawdict = _psplatform.net_io_counters()
    if not rawdict:
        return {} if pernic else None
    if nowrap:
        rawdict = _wrap_numbers(rawdict, 'psutil.net_io_counters')
    if pernic:
        for nic, fields in rawdict.items():
            rawdict[nic] = _ntp.snetio(*fields)
        return rawdict
    else:
        return _ntp.snetio(*[sum(x) for x in zip(*rawdict.values())])

