
def sync_do_join(
    eval_ctx: "EvalContext",
    value: t.Iterable[t.Any],
    d: str = "",
    attribute: t.Optional[t.Union[str, int]] = None,
) -> str:
    """Return a string which is the concatenation of the strings in the
    sequence. The separator between elements is an empty string per
    default, you can define it with the optional parameter:

    .. sourcecode:: jinja

        {{ [1, 2, 3]|join('|') }}
            -> 1|2|3

        {{ [1, 2, 3]|join }}
            -> 123

    It is also possible to join certain attributes of an object:

    .. sourcecode:: jinja

        {{ users|join(', ', attribute='username') }}

    .. versionadded:: 2.6
       The `attribute` parameter was added.
    """
    if attribute is not None:
        value = map(make_attrgetter(eval_ctx.environment, attribute), value)

    # no automatic escaping?  joining is a lot easier then
    if not eval_ctx.autoescape:
        return str(d).join(map(str, value))

    # if the delimiter doesn't have an html representation we check
    # if any of the items has.  If yes we do a coercion to Markup
    if not hasattr(d, "__html__"):
        value = list(value)
        do_escape = False

        for idx, item in enumerate(value):
            if hasattr(item, "__html__"):
                do_escape = True
            else:
                value[idx] = str(item)

        if do_escape:
            d = escape(d)
        else:
            d = str(d)

        return d.join(value)

    # no html involved, to normal joining
    return soft_str(d).join(map(soft_str, value))

