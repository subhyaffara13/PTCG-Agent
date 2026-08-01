
def _parse_composites(fh: BinaryIO) -> dict[bytes, list[CompositePart]]:
    """
    Parse the given filehandle for composites information.

    It is assumed that the file cursor is on the line behind 'StartComposites'.

    Returns
    -------
    dict
        A dict mapping composite character names to a parts list. The parts
        list is a list of `.CompositePart` entries describing the parts of
        the composite.

    Examples
    --------
    A composite definition line::

      CC Aacute 2 ; PCC A 0 0 ; PCC acute 160 170 ;

    will be represented as::

      composites[b'Aacute'] = [CompositePart(name=b'A', dx=0, dy=0),
                               CompositePart(name=b'acute', dx=160, dy=170)]

    """
    composites: dict[bytes, list[CompositePart]] = {}
    for line in fh:
        line = line.rstrip()
        if not line:
            continue
        if line.startswith(b'EndComposites'):
            return composites
        vals = line.split(b';')
        cc = vals[0].split()
        name, _num_parts = cc[1], _to_int(cc[2])
        if len(vals) != _num_parts + 2:  # First element is 'CC', last is empty.
            raise RuntimeError(f'Bad composites parse: expected {_num_parts} parts, '
                               f'but got {len(vals) - 2}')
        pccParts = []
        for s in vals[1:-1]:
            pcc = s.split()
            part = CompositePart(pcc[1], _to_float(pcc[2]), _to_float(pcc[3]))
            pccParts.append(part)
        composites[name] = pccParts

    raise RuntimeError('Bad composites parse')

