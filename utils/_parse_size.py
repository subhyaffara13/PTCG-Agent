
def _parse_size(size_str):
    """Convert memory size strings ('12 GB' etc.) to float"""
    suffixes = {
        "": 1,
        "b": 1,
        "k": 1000,
        "m": 1000**2,
        "g": 1000**3,
        "t": 1000**4,
        "kb": 1000,
        "mb": 1000**2,
        "gb": 1000**3,
        "tb": 1000**4,
        "kib": 1024,
        "mib": 1024**2,
        "gib": 1024**3,
        "tib": 1024**4,
    }

    size_re = re.compile(
        r"^\s*(\d+|\d+\.\d+)\s*({})\s*$".format("|".join(suffixes.keys())),
        re.IGNORECASE,
    )

    m = size_re.match(size_str.lower())
    if not m or m.group(2) not in suffixes:
        raise ValueError(f"value {size_str!r} not a valid size")
    return int(float(m.group(1)) * suffixes[m.group(2)])


def _parse_size(size_str):
    suffixes = {'': 1e6,
                'b': 1.0,
                'k': 1e3, 'M': 1e6, 'G': 1e9, 'T': 1e12,
                'kb': 1e3, 'Mb': 1e6, 'Gb': 1e9, 'Tb': 1e12,
                'kib': 1024.0, 'Mib': 1024.0**2, 'Gib': 1024.0**3, 'Tib': 1024.0**4}
    m = re.match(r'^\s*(\d+)\s*({})\s*$'.format('|'.join(suffixes.keys())),
                 size_str,
                 re.I)
    if not m or m.group(2) not in suffixes:
        raise ValueError("Invalid size string")

    return float(m.group(1)) * suffixes[m.group(2)]


def _parse_size(size_str):
    """Convert memory size strings ('12 GB' etc.) to float"""
    suffixes = {'': 1, 'b': 1,
                'k': 1000, 'm': 1000**2, 'g': 1000**3, 't': 1000**4,
                'kb': 1000, 'mb': 1000**2, 'gb': 1000**3, 'tb': 1000**4,
                'kib': 1024, 'mib': 1024**2, 'gib': 1024**3, 'tib': 1024**4}

    pipe_suffixes = "|".join(suffixes.keys())

    size_re = re.compile(fr'^\s*(\d+|\d+\.\d+)\s*({pipe_suffixes})\s*$', re.I)

    m = size_re.match(size_str.lower())
    if not m or m.group(2) not in suffixes:
        raise ValueError(f'value {size_str!r} not a valid size')
    return int(float(m.group(1)) * suffixes[m.group(2)])

