
def do_xmlattr(
    eval_ctx: "EvalContext", d: t.Mapping[str, t.Any], autospace: bool = True
) -> str:
    """Create an SGML/XML attribute string based on the items in a dict.

    **Values** that are neither ``none`` nor ``undefined`` are automatically
    escaped, safely allowing untrusted user input.

    User input should not be used as **keys** to this filter. If any key
    contains a space, ``/`` solidus, ``>`` greater-than sign, or ``=`` equals
    sign, this fails with a ``ValueError``. Regardless of this, user input
    should never be used as keys to this filter, or must be separately validated
    first.

    .. sourcecode:: html+jinja

        <ul{{ {'class': 'my_list', 'missing': none,
                'id': 'list-%d'|format(variable)}|xmlattr }}>
        ...
        </ul>

    Results in something like this:

    .. sourcecode:: html

        <ul class="my_list" id="list-42">
        ...
        </ul>

    As you can see it automatically prepends a space in front of the item
    if the filter returned something unless the second parameter is false.

    .. versionchanged:: 3.1.4
        Keys with ``/`` solidus, ``>`` greater-than sign, or ``=`` equals sign
        are not allowed.

    .. versionchanged:: 3.1.3
        Keys with spaces are not allowed.
    """
    items = []

    for key, value in d.items():
        if value is None or isinstance(value, Undefined):
            continue

        if _attr_key_re.search(key) is not None:
            raise ValueError(f"Invalid character in attribute name: {key!r}")

        items.append(f'{escape(key)}="{escape(value)}"')

    rv = " ".join(items)

    if autospace and rv:
        rv = " " + rv

    if eval_ctx.autoescape:
        rv = Markup(rv)

    return rv

