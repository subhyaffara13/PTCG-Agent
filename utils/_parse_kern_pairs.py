
def _parse_kern_pairs(fh: BinaryIO) -> dict[tuple[str, str], float]:
    """
    Return a kern pairs dictionary.

    Returns
    -------
    dict
        Keys are (*char1*, *char2*) tuples and values are the kern pair value. For
        example, a kern pairs line like ``KPX A y -50`` will be represented as::

            d['A', 'y'] = -50
    """
    line = next(fh)
    if not line.startswith(b'StartKernPairs'):
        raise RuntimeError(f'Bad start of kern pairs data: {line!r}')

    d: dict[tuple[str, str], float] = {}
    for line in fh:
        line = line.rstrip()
        if not line:
            continue
        if line.startswith(b'EndKernPairs'):
            next(fh)  # EndKernData
            return d
        vals = line.split()
        if len(vals) != 4 or vals[0] != b'KPX':
            raise RuntimeError(f'Bad kern pairs line: {line!r}')
        c1, c2, val = _to_str(vals[1]), _to_str(vals[2]), _to_float(vals[3])
        d[(c1, c2)] = val
    raise RuntimeError('Bad kern pairs parse')

