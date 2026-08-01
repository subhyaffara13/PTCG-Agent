
def do_replace(
    eval_ctx: "EvalContext", s: str, old: str, new: str, count: t.Optional[int] = None
) -> str:
    """Return a copy of the value with all occurrences of a substring
    replaced with a new one. The first argument is the substring
    that should be replaced, the second is the replacement string.
    If the optional third argument ``count`` is given, only the first
    ``count`` occurrences are replaced:

    .. sourcecode:: jinja

        {{ "Hello World"|replace("Hello", "Goodbye") }}
            -> Goodbye World

        {{ "aaaaargh"|replace("a", "d'oh, ", 2) }}
            -> d'oh, d'oh, aaargh
    """
    if count is None:
        count = -1

    if not eval_ctx.autoescape:
        return str(s).replace(str(old), str(new), count)

    if (
        hasattr(old, "__html__")
        or hasattr(new, "__html__")
        and not hasattr(s, "__html__")
    ):
        s = escape(s)
    else:
        s = soft_str(s)

    return s.replace(soft_str(old), soft_str(new), count)

