
def parse_csp_header(
    value: str | None,
    on_update: t.Callable[[ds.ContentSecurityPolicy], None] | None = None,
) -> ds.ContentSecurityPolicy: ...


def parse_csp_header(
    value: str | None,
    on_update: t.Callable[[ds.ContentSecurityPolicy], None] | None = None,
    cls: type[_TAnyCSP] = ...,
) -> _TAnyCSP: ...


def parse_csp_header(
    value: str | None,
    on_update: t.Callable[[ds.ContentSecurityPolicy], None] | None = None,
    cls: type[_TAnyCSP] | None = None,
) -> _TAnyCSP:
    """Parse a Content Security Policy header.

    .. versionadded:: 1.0.0
       Support for Content Security Policy headers was added.

    :param value: a csp header to be parsed.
    :param on_update: an optional callable that is called every time a value
                      on the object is changed.
    :param cls: the class for the returned object.  By default
                :class:`~werkzeug.datastructures.ContentSecurityPolicy` is used.
    :return: a `cls` object.
    """
    if cls is None:
        cls = t.cast("type[_TAnyCSP]", ds.ContentSecurityPolicy)

    if value is None:
        return cls((), on_update)

    items = []

    for policy in value.split(";"):
        policy = policy.strip()

        # Ignore badly formatted policies (no space)
        if " " in policy:
            directive, value = policy.strip().split(" ", 1)
            items.append((directive.strip(), value.strip()))

    return cls(items, on_update)

