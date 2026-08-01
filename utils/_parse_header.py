
def _parse_header(fh: BinaryIO) -> FontMetricsHeader:
    """
    Read the font metrics header (up to the char metrics).

    Returns
    -------
    dict
        A dictionary mapping *key* to *val*. Dictionary keys are:

            StartFontMetrics, FontName, FullName, FamilyName, Weight, ItalicAngle,
            IsFixedPitch, FontBBox, UnderlinePosition, UnderlineThickness, Version,
            Notice, EncodingScheme, CapHeight, XHeight, Ascender, Descender,
            StartCharMetrics

        *val* will be converted to the appropriate Python type as necessary, e.g.,:

            * 'False' -> False
            * '0' -> 0
            * '-168 -218 1000 898' -> [-168, -218, 1000, 898]
    """
    header_converters = {
        bool: _to_bool,
        bytes: lambda x: x,
        float: _to_float,
        int: _to_int,
        list[int]: _to_list_of_ints,
        str: _to_str,
    }
    header_value_types = inspect.get_annotations(FontMetricsHeader)
    d: FontMetricsHeader = {}
    first_line = True
    for line in fh:
        line = line.rstrip()
        if line.startswith(b'Comment'):
            continue
        lst = line.split(b' ', 1)
        key = lst[0]
        if first_line:
            # AFM spec, Section 4: The StartFontMetrics keyword
            # [followed by a version number] must be the first line in
            # the file, and the EndFontMetrics keyword must be the
            # last non-empty line in the file.  We just check the
            # first header entry.
            if key != b'StartFontMetrics':
                raise RuntimeError('Not an AFM file')
            first_line = False
        if len(lst) == 2:
            val = lst[1]
        else:
            val = b''
        try:
            key_str = _to_str(key)
            value_type = header_value_types[key_str]
        except (KeyError, UnicodeDecodeError):
            _log.error("Found an unknown keyword in AFM header (was %r)", key)
            continue
        try:
            converter = header_converters[value_type]
            d[key_str] = converter(val)  # type: ignore[literal-required]
        except ValueError:
            _log.error('Value error parsing header in AFM: %r, %r', key, val)
            continue
        if key == b'StartCharMetrics':
            break
    else:
        raise RuntimeError('Bad parse')
    return d

