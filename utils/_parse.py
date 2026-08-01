
def _parse(markup: str) -> Iterable[Tuple[int, Optional[str], Optional[Tag]]]:
    """Parse markup in to an iterable of tuples of (position, text, tag).

    Args:
        markup (str): A string containing console markup

    """
    position = 0
    _divmod = divmod
    _Tag = Tag
    for match in RE_TAGS.finditer(markup):
        full_text, escapes, tag_text = match.groups()
        start, end = match.span()
        if start > position:
            yield start, markup[position:start], None
        if escapes:
            backslashes, escaped = _divmod(len(escapes), 2)
            if backslashes:
                # Literal backslashes
                yield start, "\\" * backslashes, None
                start += backslashes * 2
            if escaped:
                # Escape of tag
                yield start, full_text[len(escapes) :], None
                position = end
                continue
        text, equals, parameters = tag_text.partition("=")
        yield start, None, _Tag(text, parameters if equals else None)
        position = end
    if position < len(markup):
        yield position, markup[position:], None


def _parse(markup: str) -> Iterable[Tuple[int, Optional[str], Optional[Tag]]]:
    """Parse markup in to an iterable of tuples of (position, text, tag).

    Args:
        markup (str): A string containing console markup

    """
    position = 0
    _divmod = divmod
    _Tag = Tag
    for match in RE_TAGS.finditer(markup):
        full_text, escapes, tag_text = match.groups()
        start, end = match.span()
        if start > position:
            yield start, markup[position:start], None
        if escapes:
            backslashes, escaped = _divmod(len(escapes), 2)
            if backslashes:
                # Literal backslashes
                yield start, "\\" * backslashes, None
                start += backslashes * 2
            if escaped:
                # Escape of tag
                yield start, full_text[len(escapes) :], None
                position = end
                continue
        text, equals, parameters = tag_text.partition("=")
        yield start, None, _Tag(text, parameters if equals else None)
        position = end
    if position < len(markup):
        yield position, markup[position:], None


def _parse(
    flavor,
    io,
    match,
    attrs,
    encoding,
    displayed_only,
    extract_links,
    storage_options,
    **kwargs,
):
    flavor = _validate_flavor(flavor)
    compiled_match = re.compile(match)  # you can pass a compiled regex here

    retained = None
    for flav in flavor:
        parser = _parser_dispatch(flav)
        p = parser(
            io,
            compiled_match,
            attrs,
            encoding,
            displayed_only,
            extract_links,
            storage_options,
        )

        try:
            tables = p.parse_tables()
        except ValueError as caught:
            # if `io` is an io-like object, check if it's seekable
            # and try to rewind it before trying the next parser
            if hasattr(io, "seekable") and io.seekable():
                io.seek(0)
            elif hasattr(io, "seekable") and not io.seekable():
                # if we couldn't rewind it, let the user know
                raise ValueError(
                    f"The flavor {flav} failed to parse your input. "
                    "Since you passed a non-rewindable file "
                    "object, we can't rewind it to try "
                    "another parser. Try read_html() with a different flavor."
                ) from caught

            retained = caught
        else:
            break
    else:
        assert retained is not None  # for mypy
        raise retained

    ret = []
    for table in tables:
        try:
            df = _data_to_frame(data=table, **kwargs)
            # Cast MultiIndex header to an Index of tuples when extracting header
            # links and replace nan with None (therefore can't use mi.to_flat_index()).
            # This maintains consistency of selection (e.g. df.columns.str[1])
            if extract_links in ("all", "header") and isinstance(
                df.columns, MultiIndex
            ):
                df.columns = Index(
                    ((col[0], None if isna(col[1]) else col[1]) for col in df.columns),
                    tupleize_cols=False,
                )

            ret.append(df)
        except EmptyDataError:  # empty table
            continue
    return ret


def _parse(
    path_or_buffer: FilePath | ReadBuffer[bytes] | ReadBuffer[str],
    xpath: str,
    namespaces: dict[str, str] | None,
    elems_only: bool,
    attrs_only: bool,
    names: Sequence[str] | None,
    dtype: DtypeArg | None,
    converters: ConvertersArg | None,
    parse_dates: ParseDatesArg | None,
    encoding: str | None,
    parser: XMLParsers,
    stylesheet: FilePath | ReadBuffer[bytes] | ReadBuffer[str] | None,
    iterparse: dict[str, list[str]] | None,
    compression: CompressionOptions,
    storage_options: StorageOptions,
    dtype_backend: DtypeBackend | lib.NoDefault = lib.no_default,
    **kwargs,
) -> DataFrame:
    """
    Call internal parsers.

    This method will conditionally call internal parsers:
    LxmlFrameParser and/or EtreeParser.

    Raises
    ------
    ImportError
        * If lxml is not installed if selected as parser.

    ValueError
        * If parser is not lxml or etree.
    """

    p: _EtreeFrameParser | _LxmlFrameParser

    if parser == "lxml":
        lxml = import_optional_dependency("lxml.etree", errors="ignore")

        if lxml is not None:
            p = _LxmlFrameParser(
                path_or_buffer,
                xpath,
                namespaces,
                elems_only,
                attrs_only,
                names,
                dtype,
                converters,
                parse_dates,
                encoding,
                stylesheet,
                iterparse,
                compression,
                storage_options,
            )
        else:
            raise ImportError("lxml not found, please install or use the etree parser.")

    elif parser == "etree":
        p = _EtreeFrameParser(
            path_or_buffer,
            xpath,
            namespaces,
            elems_only,
            attrs_only,
            names,
            dtype,
            converters,
            parse_dates,
            encoding,
            stylesheet,
            iterparse,
            compression,
            storage_options,
        )
    else:
        raise ValueError("Values for parser can only be lxml or etree.")

    data_dicts = p.parse_data()

    return _data_to_frame(
        data=data_dicts,
        dtype=dtype,
        converters=converters,
        parse_dates=parse_dates,
        dtype_backend=dtype_backend,
        **kwargs,
    )

