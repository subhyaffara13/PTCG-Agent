
def parse_cache_control_header(
    value: str | None,
    on_update: t.Callable[[ds.cache_control._CacheControl], None] | None = None,
) -> ds.RequestCacheControl: ...


def parse_cache_control_header(
    value: str | None,
    on_update: t.Callable[[ds.cache_control._CacheControl], None] | None = None,
    cls: type[_TAnyCC] = ...,
) -> _TAnyCC: ...


def parse_cache_control_header(
    value: str | None,
    on_update: t.Callable[[ds.cache_control._CacheControl], None] | None = None,
    cls: type[_TAnyCC] | None = None,
) -> _TAnyCC:
    """Parse a cache control header.  The RFC differs between response and
    request cache control, this method does not.  It's your responsibility
    to not use the wrong control statements.

    .. versionadded:: 0.5
       The `cls` was added.  If not specified an immutable
       :class:`~werkzeug.datastructures.RequestCacheControl` is returned.

    :param value: a cache control header to be parsed.
    :param on_update: an optional callable that is called every time a value
                      on the :class:`~werkzeug.datastructures.CacheControl`
                      object is changed.
    :param cls: the class for the returned object.  By default
                :class:`~werkzeug.datastructures.RequestCacheControl` is used.
    :return: a `cls` object.
    """
    if cls is None:
        cls = t.cast("type[_TAnyCC]", ds.RequestCacheControl)

    if not value:
        return cls((), on_update)

    return cls(parse_dict_header(value), on_update)

