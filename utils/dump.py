
def dump(obj, file, protocol=None, buffer_callback=None):
    """Serialize obj as bytes streamed into file

    protocol defaults to cloudpickle.DEFAULT_PROTOCOL which is an alias to
    pickle.HIGHEST_PROTOCOL. This setting favors maximum communication
    speed between processes running the same Python version.

    Set protocol=pickle.DEFAULT_PROTOCOL instead if you need to ensure
    compatibility with older versions of Python (although this is not always
    guaranteed to work because cloudpickle relies on some internal
    implementation details that can change from one Python version to the
    next).
    """
    Pickler(file, protocol=protocol, buffer_callback=buffer_callback).dump(obj)


def dump(object, **kwds):
    """dill.dump of object to a NamedTemporaryFile.
Loads with "dill.temp.load".  Returns the filehandle.

    >>> dumpfile = dill.temp.dump([1, 2, 3, 4, 5])
    >>> dill.temp.load(dumpfile)
    [1, 2, 3, 4, 5]

Optional kwds:
    If 'suffix' is specified, the file name will end with that suffix,
    otherwise there will be no suffix.
    
    If 'prefix' is specified, the file name will begin with that prefix,
    otherwise a default prefix is used.
    
    If 'dir' is specified, the file will be created in that directory,
    otherwise a default directory is used.
    
    If 'text' is specified and true, the file is opened in text
    mode.  Else (the default) the file is opened in binary mode.  On
    some operating systems, this makes no difference.

NOTE: Keep the return value for as long as you want your file to exist !
    """
    import dill as pickle
    import tempfile
    kwds.setdefault('delete', True)
    file = tempfile.NamedTemporaryFile(**kwds)
    pickle.dump(object, file)
    file.flush()
    return file


def dump(obj, file, protocol=None, byref=None, fmode=None, recurse=None, **kwds):#, strictio=None):
    """
    Pickle an object to a file.

    See :func:`dumps` for keyword arguments.
    """
    from .settings import settings
    protocol = settings['protocol'] if protocol is None else int(protocol)
    _kwds = kwds.copy()
    _kwds.update(dict(byref=byref, fmode=fmode, recurse=recurse))
    Pickler(file, protocol, **_kwds).dump(obj)
    return


def dump(obj, fp, skipkeys=False, ensure_ascii=True, check_circular=True,
         allow_nan=False, cls=None, indent=None, separators=None,
         encoding='utf-8', default=None, use_decimal=True,
         namedtuple_as_object=True, tuple_as_array=True,
         bigint_as_string=False, sort_keys=False, item_sort_key=None,
         for_json=False, ignore_nan=False, int_as_string_bitcount=None,
         iterable_as_array=False, **kw):
    """Serialize ``obj`` as a JSON formatted stream to ``fp`` (a
    ``.write()``-supporting file-like object).

    If *skipkeys* is true then ``dict`` keys that are not basic types
    (``str``, ``int``, ``long``, ``float``, ``bool``, ``None``)
    will be skipped instead of raising a ``TypeError``.

    If *ensure_ascii* is false (default: ``True``), then the output may
    contain non-ASCII characters, so long as they do not need to be escaped
    by JSON. When it is true, all non-ASCII characters are escaped.

    If *allow_nan* is true (default: ``False``), then out of range ``float``
    values (``nan``, ``inf``, ``-inf``) will be serialized to
    their JavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``)
    instead of raising a ValueError. See
    *ignore_nan* for ECMA-262 compliant behavior.

    If *indent* is a string, then JSON array elements and object members
    will be pretty-printed with a newline followed by that string repeated
    for each level of nesting. ``None`` (the default) selects the most compact
    representation without any newlines.

    If specified, *separators* should be an
    ``(item_separator, key_separator)`` tuple.  The default is ``(', ', ': ')``
    if *indent* is ``None`` and ``(',', ': ')`` otherwise.  To get the most
    compact JSON representation, you should specify ``(',', ':')`` to eliminate
    whitespace.

    *encoding* is the character encoding for str instances, default is UTF-8.

    *default(obj)* is a function that should return a serializable version
    of obj or raise ``TypeError``. The default simply raises ``TypeError``.

    If *use_decimal* is true (default: ``True``) then decimal.Decimal
    will be natively serialized to JSON with full precision.

    If *namedtuple_as_object* is true (default: ``True``),
    :class:`tuple` subclasses with ``_asdict()`` methods will be encoded
    as JSON objects.

    If *tuple_as_array* is true (default: ``True``),
    :class:`tuple` (and subclasses) will be encoded as JSON arrays.

    If *iterable_as_array* is true (default: ``False``),
    any object not in the above table that implements ``__iter__()``
    will be encoded as a JSON array.

    If *bigint_as_string* is true (default: ``False``), ints 2**53 and higher
    or lower than -2**53 will be encoded as strings. This is to avoid the
    rounding that happens in Javascript otherwise. Note that this is still a
    lossy operation that will not round-trip correctly and should be used
    sparingly.

    If *int_as_string_bitcount* is a positive number (n), then int of size
    greater than or equal to 2**n or lower than or equal to -2**n will be
    encoded as strings.

    If specified, *item_sort_key* is a callable used to sort the items in
    each dictionary. This is useful if you want to sort items other than
    in alphabetical order by key. This option takes precedence over
    *sort_keys*.

    If *sort_keys* is true (default: ``False``), the output of dictionaries
    will be sorted by item.

    If *for_json* is true (default: ``False``), objects with a ``for_json()``
    method will use the return value of that method for encoding as JSON
    instead of the object.

    If *ignore_nan* is true (default: ``False``), then out of range
    :class:`float` values (``nan``, ``inf``, ``-inf``) will be serialized as
    ``null`` in compliance with the ECMA-262 specification. If true, this will
    override *allow_nan*.

    To use a custom ``JSONEncoder`` subclass (e.g. one that overrides the
    ``.default()`` method to serialize additional types), specify it with
    the ``cls`` kwarg. NOTE: You should use *default* or *for_json* instead
    of subclassing whenever possible.

    """
    # cached encoder
    if (not skipkeys and ensure_ascii and
        check_circular and not allow_nan and
        cls is None and indent is None and separators is None and
        encoding == 'utf-8' and default is None and use_decimal
        and namedtuple_as_object and tuple_as_array and not iterable_as_array
        and not bigint_as_string and not sort_keys
        and not item_sort_key and not for_json
        and not ignore_nan and int_as_string_bitcount is None
        and not kw
    ):
        iterable = _default_encoder.iterencode(obj)
    else:
        if cls is None:
            cls = JSONEncoder
        iterable = cls(skipkeys=skipkeys, ensure_ascii=ensure_ascii,
            check_circular=check_circular, allow_nan=allow_nan, indent=indent,
            separators=separators, encoding=encoding,
            default=default, use_decimal=use_decimal,
            namedtuple_as_object=namedtuple_as_object,
            tuple_as_array=tuple_as_array,
            iterable_as_array=iterable_as_array,
            bigint_as_string=bigint_as_string,
            sort_keys=sort_keys,
            item_sort_key=item_sort_key,
            for_json=for_json,
            ignore_nan=ignore_nan,
            int_as_string_bitcount=int_as_string_bitcount,
            **kw).iterencode(obj)
    # could accelerate with writelines in some versions of Python, at
    # a debuggability cost
    for chunk in iterable:
        fp.write(chunk)


def dump(
    obj: Mapping[str, Any],
    fp: IO[bytes],
    /,
    *,
    multiline_strings: bool = False,
    indent: int = 4,
) -> None:
    ctx = Context(multiline_strings, indent)
    for chunk in gen_table_chunks(obj, ctx, name=""):
        fp.write(chunk.encode())


def dump(data: Mapping[str, Any], fp: IO[str], *, sort_keys: bool = False) -> None:
    """
    Dump a TOMLDocument into a writable file stream.

    :param data: a dict-like object to dump
    :param sort_keys: if true, sort the keys in alphabetic order

    :Example:

    >>> with open("output.toml", "w") as fp:
    ...     tomlkit.dump(data, fp)
    """
    fp.write(dumps(data, sort_keys=sort_keys))


def dump(data, stream=None, Dumper=Dumper, **kwds):
    """
    Serialize a Python object into a YAML stream.
    If stream is None, return the produced string instead.
    """
    return dump_all([data], stream, Dumper=Dumper, **kwds)


def dump(obj: object = missing) -> None:
    """Print the object details to stdout._write (for the interactive
    console of the web debugger.
    """
    gen = DebugReprGenerator()
    if obj is missing:
        rv = gen.dump_locals(sys._getframe(1).f_locals)
    else:
        rv = gen.dump_object(obj)
    sys.stdout._write(rv)  # type: ignore


def dump():
    """Store the current runtime db state to the module file."""
    current_file = inspect.getfile(dump)
    with open(current_file) as f:
        current_content = f.read()
    begin_data_str = "# BEGIN GENERATED DATA\n"
    begin_data_index = current_content.find(begin_data_str)
    end_data_index = current_content.find("    # END GENERATED DATA\n")
    if begin_data_index == -1 or end_data_index == -1:
        warnings.warn(
            f"{current_file} cannot be updated:"
            " BEGIN/END GENERATED DATA comment blocks appear to be corrupted",
            stacklevel=2,
        )
        return

    def sort_key(key):
        op, device_name, version = key
        version = tuple(
            (str(item) if isinstance(item, torch.dtype) else item) for item in version
        )
        return (op, device_name, version)

    part1 = current_content[: begin_data_index + len(begin_data_str)]
    part2 = current_content[end_data_index:]
    data_part = []
    for op_key in sorted(_operation_device_version_data, key=sort_key):
        data_part.append("    " + repr(op_key).replace("'", '"') + ": {")
        op_data = _operation_device_version_data[op_key]
        data_part.extend(f"        {key}: {op_data[key]}," for key in sorted(op_data))
        data_part.append("    },")
    new_content = part1 + "\n".join(data_part) + "\n" + part2
    if current_content != new_content:
        with open(current_file, "w") as f:
            f.write(new_content)


def dump(dot_file_name: str):
    """Dump TrieCache in the dot format"""
    return torch._C._lazy._dump_ir_cache(dot_file_name)


def dump(
    obj: Mapping[str, Any],
    fp: IO[bytes],
    /,
    *,
    multiline_strings: bool = False,
    indent: int = 4,
) -> None:
    ctx = Context(multiline_strings, indent)
    for chunk in gen_table_chunks(obj, ctx, name=""):
        fp.write(chunk.encode())


def dump(
    value: PlistEncodable,
    fp: IO[bytes],
    sort_keys: bool = True,
    skipkeys: bool = False,
    use_builtin_types: Optional[bool] = None,
    pretty_print: bool = True,
) -> None:
    """Write a Python object to a plist file.

    Args:
        value: An object to write.
        fp: A file opened for writing.
        sort_keys (bool): Whether keys of dictionaries should be sorted.
        skipkeys (bool): Whether to silently skip non-string dictionary
            keys.
        use_builtin_types (bool): If true, byte strings will be
            encoded in Base-64 and wrapped in a ``data`` tag; if
            false, they will be either stored as ASCII strings or an
            exception raised if they cannot be represented. Defaults
        pretty_print (bool): Whether to indent the output.
        indent_level (int): Level of indentation when serializing.

    Raises:
        ``TypeError``
            if non-string dictionary keys are serialized
            and ``skipkeys`` is false.
        ``ValueError``
            if non-representable binary data is present
            and `use_builtin_types` is false.
    """

    if not hasattr(fp, "write"):
        raise AttributeError("'%s' object has no attribute 'write'" % type(fp).__name__)
    root = etree.Element("plist", version="1.0")
    el = totree(
        value,
        sort_keys=sort_keys,
        skipkeys=skipkeys,
        use_builtin_types=use_builtin_types,
        pretty_print=pretty_print,
    )
    root.append(el)
    tree = etree.ElementTree(root)
    # we write the doctype ourselves instead of using the 'doctype' argument
    # of 'write' method, becuse lxml will force adding a '\n' even when
    # pretty_print is False.
    if pretty_print:
        header = b"\n".join((XML_DECLARATION, PLIST_DOCTYPE, b""))
    else:
        header = XML_DECLARATION + PLIST_DOCTYPE
    fp.write(header)
    tree.write(  # type: ignore
        fp,
        encoding="utf-8",
        pretty_print=pretty_print,
        xml_declaration=False,
    )


def dump(obj: t.Any, fp: t.IO[str], **kwargs: t.Any) -> None:
    """Serialize data as JSON and write to a file.

    If :data:`~flask.current_app` is available, it will use its
    :meth:`app.json.dump() <flask.json.provider.JSONProvider.dump>`
    method, otherwise it will use :func:`json.dump`.

    :param obj: The data to serialize.
    :param fp: A file opened for writing text. Should use the UTF-8
        encoding to be valid JSON.
    :param kwargs: Arguments passed to the ``dump`` implementation.

    .. versionchanged:: 2.3
        The ``app`` parameter was removed.

    .. versionchanged:: 2.2
        Calls ``current_app.json.dump``, allowing an app to override
        the behavior.

    .. versionchanged:: 2.0
        Writing to a binary file, and the ``encoding`` argument, will be
        removed in Flask 2.1.
    """
    if current_app:
        current_app.json.dump(obj, fp, **kwargs)
    else:
        kwargs.setdefault("default", _default)
        _json.dump(obj, fp, **kwargs)

