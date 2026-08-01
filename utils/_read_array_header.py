
def _read_array_header(fp, version, max_header_size=_MAX_HEADER_SIZE):
    """
    see read_array_header_1_0
    """
    # Read an unsigned, little-endian short int which has the length of the
    # header.
    import ast
    import struct
    hinfo = _header_size_info.get(version)
    if hinfo is None:
        raise ValueError(f"Invalid version {version!r}")
    hlength_type, encoding = hinfo

    hlength_str = _read_bytes(fp, struct.calcsize(hlength_type), "array header length")
    header_length = struct.unpack(hlength_type, hlength_str)[0]
    header = _read_bytes(fp, header_length, "array header")
    header = header.decode(encoding)
    if len(header) > max_header_size:
        raise ValueError(
            f"Header info length ({len(header)}) is large and may not be safe "
            "to load securely.\n"
            "To allow loading, adjust `max_header_size` or fully trust "
            "the `.npy` file using `allow_pickle=True`.\n"
            "For safety against large resource use or crashes, sandboxing "
            "may be necessary.")

    # The header is a pretty-printed string representation of a literal
    # Python dictionary with trailing newlines padded to an ARRAY_ALIGN byte
    # boundary. The keys are strings.
    #   "shape" : tuple of int
    #   "fortran_order" : bool
    #   "descr" : dtype.descr
    # Versions (2, 0) and (1, 0) could have been created by a Python 2
    # implementation before header filtering was implemented.
    #
    # For performance reasons, we try without _filter_header first though
    try:
        d = ast.literal_eval(header)
    except SyntaxError as e:
        if version <= (2, 0):
            header = _filter_header(header)
            try:
                d = ast.literal_eval(header)
            except SyntaxError as e2:
                msg = "Cannot parse header: {!r}"
                raise ValueError(msg.format(header)) from e2
            else:
                warnings.warn(
                    "Reading `.npy` or `.npz` file required additional "
                    "header parsing as it was created on Python 2. Save the "
                    "file again to speed up loading and avoid this warning.",
                    UserWarning, stacklevel=4)
        else:
            msg = "Cannot parse header: {!r}"
            raise ValueError(msg.format(header)) from e
    if not isinstance(d, dict):
        msg = "Header is not a dictionary: {!r}"
        raise ValueError(msg.format(d))

    if EXPECTED_KEYS != d.keys():
        keys = sorted(d.keys())
        msg = "Header does not contain the correct keys: {!r}"
        raise ValueError(msg.format(keys))

    # Sanity-check the values.
    if (not isinstance(d['shape'], tuple) or
            not all(isinstance(x, int) for x in d['shape'])):
        msg = "shape is not valid: {!r}"
        raise ValueError(msg.format(d['shape']))
    if not isinstance(d['fortran_order'], bool):
        msg = "fortran_order is not a valid bool: {!r}"
        raise ValueError(msg.format(d['fortran_order']))
    try:
        dtype = descr_to_dtype(d['descr'])
    except TypeError as e:
        msg = "descr is not a valid dtype descriptor: {!r}"
        raise ValueError(msg.format(d['descr'])) from e

    return d['shape'], d['fortran_order'], dtype

