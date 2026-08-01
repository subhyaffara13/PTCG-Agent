
def dumps(obj, protocol=None, buffer_callback=None):
    """Serialize obj as a string of bytes allocated in memory

    protocol defaults to cloudpickle.DEFAULT_PROTOCOL which is an alias to
    pickle.HIGHEST_PROTOCOL. This setting favors maximum communication
    speed between processes running the same Python version.

    Set protocol=pickle.DEFAULT_PROTOCOL instead if you need to ensure
    compatibility with older versions of Python (although this is not always
    guaranteed to work because cloudpickle relies on some internal
    implementation details that can change from one Python version to the
    next).
    """
    with io.BytesIO() as file:
        cp = Pickler(file, protocol=protocol, buffer_callback=buffer_callback)
        cp.dump(obj)
        return file.getvalue()


def dumps(obj, protocol=None, byref=None, fmode=None, recurse=None, **kwds):#, strictio=None):
    """
    Pickle an object to a string.

    *protocol* is the pickler protocol, as defined for Python *pickle*.

    If *byref=True*, then dill behaves a lot more like pickle as certain
    objects (like modules) are pickled by reference as opposed to attempting
    to pickle the object itself.

    If *recurse=True*, then objects referred to in the global dictionary
    are recursively traced and pickled, instead of the default behavior
    of attempting to store the entire global dictionary. This is needed for
    functions defined via *exec()*.

    *fmode* (:const:`HANDLE_FMODE`, :const:`CONTENTS_FMODE`,
    or :const:`FILE_FMODE`) indicates how file handles will be pickled.
    For example, when pickling a data file handle for transfer to a remote
    compute service, *FILE_FMODE* will include the file contents in the
    pickle and cursor position so that a remote method can operate
    transparently on an object with an open file handle.

    Default values for keyword arguments can be set in :mod:`dill.settings`.
    """
    file = StringIO()
    dump(obj, file, protocol, byref, fmode, recurse, **kwds)#, strictio)
    return file.getvalue()


def Dumps(obj):
  """Returns bytearray with the encoded python object."""
  fbb = Builder()
  fbb.Add(obj)
  return fbb.Finish()


def dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
          allow_nan=False, cls=None, indent=None, separators=None,
          encoding='utf-8', default=None, use_decimal=True,
          namedtuple_as_object=True, tuple_as_array=True,
          bigint_as_string=False, sort_keys=False, item_sort_key=None,
          for_json=False, ignore_nan=False, int_as_string_bitcount=None,
          iterable_as_array=False, **kw):
    """Serialize ``obj`` to a JSON formatted ``str``.

    If ``skipkeys`` is true then ``dict`` keys that are not basic types
    (``str``, ``int``, ``long``, ``float``, ``bool``, ``None``)
    will be skipped instead of raising a ``TypeError``.

    If *ensure_ascii* is false (default: ``True``), then the output may
    contain non-ASCII characters, so long as they do not need to be escaped
    by JSON. When it is true, all non-ASCII characters are escaped.

    If ``check_circular`` is false, then the circular reference check
    for container types will be skipped and a circular reference will
    result in an ``OverflowError`` (or worse).

    If *allow_nan* is true (default: ``False``), then out of range ``float``
    values (``nan``, ``inf``, ``-inf``) will be serialized to
    their JavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``)
    instead of raising a ValueError. See
    *ignore_nan* for ECMA-262 compliant behavior.

    If ``indent`` is a string, then JSON array elements and object members
    will be pretty-printed with a newline followed by that string repeated
    for each level of nesting. ``None`` (the default) selects the most compact
    representation without any newlines. For backwards compatibility with
    versions of simplejson earlier than 2.1.0, an integer is also accepted
    and is converted to a string with that many spaces.

    If specified, ``separators`` should be an
    ``(item_separator, key_separator)`` tuple.  The default is ``(', ', ': ')``
    if *indent* is ``None`` and ``(',', ': ')`` otherwise.  To get the most
    compact JSON representation, you should specify ``(',', ':')`` to eliminate
    whitespace.

    ``encoding`` is the character encoding for bytes instances, default is
    UTF-8.

    ``default(obj)`` is a function that should return a serializable version
    of obj or raise TypeError. The default simply raises TypeError.

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

    If *bigint_as_string* is true (not the default), ints 2**53 and higher
    or lower than -2**53 will be encoded as strings. This is to avoid the
    rounding that happens in Javascript otherwise.

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
    the ``cls`` kwarg. NOTE: You should use *default* instead of subclassing
    whenever possible.

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
        return _default_encoder.encode(obj)
    if cls is None:
        cls = JSONEncoder
    return cls(
        skipkeys=skipkeys, ensure_ascii=ensure_ascii,
        check_circular=check_circular, allow_nan=allow_nan, indent=indent,
        separators=separators, encoding=encoding, default=default,
        use_decimal=use_decimal,
        namedtuple_as_object=namedtuple_as_object,
        tuple_as_array=tuple_as_array,
        iterable_as_array=iterable_as_array,
        bigint_as_string=bigint_as_string,
        sort_keys=sort_keys,
        item_sort_key=item_sort_key,
        for_json=for_json,
        ignore_nan=ignore_nan,
        int_as_string_bitcount=int_as_string_bitcount,
        **kw).encode(obj)


def dumps(
    obj: Mapping[str, Any], /, *, multiline_strings: bool = False, indent: int = 4
) -> str:
    ctx = Context(multiline_strings, indent)
    return "".join(gen_table_chunks(obj, ctx, name=""))


def dumps(data: Mapping[str, Any], sort_keys: bool = False) -> str:
    """
    Dumps a TOMLDocument into a string.
    """
    if isinstance(data, (Table, InlineTable, Container)):
        if not sort_keys:
            return data.as_string()

        return item(data, _sort_keys=True).as_string()

    if isinstance(data, Mapping):
        return item(dict(data), _sort_keys=sort_keys).as_string()

    try:
        # mapping-like wrappers (e.g. dotty_dict's Dotty) delegate
        # ``as_string`` to the document they wrap; rendering it directly
        # preserves the original layout, which re-encoding through a plain
        # dict would lose
        return data.as_string()  # type: ignore[attr-defined]
    except AttributeError as ex:
        msg = f"Expecting Mapping or TOML Table or Container, {type(data)} given"
        raise TypeError(msg) from ex


def dumps(
    obj: Mapping[str, Any], /, *, multiline_strings: bool = False, indent: int = 4
) -> str:
    ctx = Context(multiline_strings, indent)
    return "".join(gen_table_chunks(obj, ctx, name=""))


def dumps(obj: Any) -> bytes:
  """See `pickle.dumps`. Used for serializing host callbacks in jaxlib."""
  if cloudpickle is None:
    raise ModuleNotFoundError('No module named "cloudpickle"')

  class Pickler(cloudpickle.CloudPickler):
    """Customizes the behavior of cloudpickle."""

    # Make a copy to avoid modifying cloudpickle for other users.
    dispatch_table = cloudpickle.CloudPickler.dispatch_table.copy()  # pyrefly: ignore[missing-attribute]

    # Fixes for dataclass internal singleton object serialization.
    # Bug: https://github.com/cloudpipe/cloudpickle/issues/386
    dispatch_table[dataclasses._FIELD_BASE] = lambda x: f'{x.name}'  # pyrefly: ignore[missing-attribute]
    dispatch_table[dataclasses._MISSING_TYPE] = lambda _: 'MISSING'
    dispatch_table[dataclasses._HAS_DEFAULT_FACTORY_CLASS] = (  # pyrefly: ignore[missing-attribute]
        lambda _: '_HAS_DEFAULT_FACTORY'
    )
    if hasattr(dataclasses, '_KW_ONLY_TYPE'):
      dispatch_table[dataclasses._KW_ONLY_TYPE] = (
          lambda _: '_KW_ONLY_TYPE'
      )  # Added in Python 3.10.

  with io.BytesIO() as file:
    Pickler(file).dump(obj)
    return file.getvalue()


def dumps(
    value: PlistEncodable,
    sort_keys: bool = True,
    skipkeys: bool = False,
    use_builtin_types: Optional[bool] = None,
    pretty_print: bool = True,
) -> bytes:
    """Write a Python object to a string in plist format.

    Args:
        value: An object to write.
        sort_keys (bool): Whether keys of dictionaries should be sorted.
        skipkeys (bool): Whether to silently skip non-string dictionary
            keys.
        use_builtin_types (bool): If true, byte strings will be
            encoded in Base-64 and wrapped in a ``data`` tag; if
            false, they will be either stored as strings or an
            exception raised if they cannot be represented. Defaults
        pretty_print (bool): Whether to indent the output.
        indent_level (int): Level of indentation when serializing.

    Returns:
        string: A plist representation of the Python object.

    Raises:
        ``TypeError``
            if non-string dictionary keys are serialized
            and ``skipkeys`` is false.
        ``ValueError``
            if non-representable binary data is present
            and `use_builtin_types` is false.
    """
    fp = BytesIO()
    dump(
        value,
        fp,
        sort_keys=sort_keys,
        skipkeys=skipkeys,
        use_builtin_types=use_builtin_types,
        pretty_print=pretty_print,
    )
    return fp.getvalue()


def dumps(obj: t.Any, **kwargs: t.Any) -> str:
    """Serialize data as JSON.

    If :data:`~flask.current_app` is available, it will use its
    :meth:`app.json.dumps() <flask.json.provider.JSONProvider.dumps>`
    method, otherwise it will use :func:`json.dumps`.

    :param obj: The data to serialize.
    :param kwargs: Arguments passed to the ``dumps`` implementation.

    .. versionchanged:: 2.3
        The ``app`` parameter was removed.

    .. versionchanged:: 2.2
        Calls ``current_app.json.dumps``, allowing an app to override
        the behavior.

    .. versionchanged:: 2.0.2
        :class:`decimal.Decimal` is supported by converting to a string.

    .. versionchanged:: 2.0
        ``encoding`` will be removed in Flask 2.1.

    .. versionchanged:: 1.0.3
        ``app`` can be passed directly, rather than requiring an app
        context for configuration.
    """
    if current_app:
        return current_app.json.dumps(obj, **kwargs)

    kwargs.setdefault("default", _default)
    return _json.dumps(obj, **kwargs)

