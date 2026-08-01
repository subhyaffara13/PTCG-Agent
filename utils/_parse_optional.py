
def _parse_optional(fh: BinaryIO) -> tuple[dict[tuple[str, str], float],
                                           dict[bytes, list[CompositePart]]]:
    """
    Parse the optional fields for kern pair data and composites.

    Returns
    -------
    kern_data : dict
        A dict containing kerning information. May be empty.
        See `._parse_kern_pairs`.
    composites : dict
        A dict containing composite information. May be empty.
        See `._parse_composites`.
    """
    kern_data: dict[tuple[str, str], float] = {}
    composites: dict[bytes, list[CompositePart]] = {}
    for line in fh:
        line = line.rstrip()
        if not line:
            continue
        match line.split()[0]:
            case b'StartKernData':
                kern_data = _parse_kern_pairs(fh)
            case b'StartComposites':
                composites = _parse_composites(fh)

    return kern_data, composites

