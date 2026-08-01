
def do_tojson(
    eval_ctx: "EvalContext", value: t.Any, indent: t.Optional[int] = None
) -> Markup:
    """Serialize an object to a string of JSON, and mark it safe to
    render in HTML. This filter is only for use in HTML documents.

    The returned string is safe to render in HTML documents and
    ``<script>`` tags. The exception is in HTML attributes that are
    double quoted; either use single quotes or the ``|forceescape``
    filter.

    :param value: The object to serialize to JSON.
    :param indent: The ``indent`` parameter passed to ``dumps``, for
        pretty-printing the value.

    .. versionadded:: 2.9
    """
    policies = eval_ctx.environment.policies
    dumps = policies["json.dumps_function"]
    kwargs = policies["json.dumps_kwargs"]

    if indent is not None:
        kwargs = kwargs.copy()
        kwargs["indent"] = indent

    return htmlsafe_json_dumps(value, dumps=dumps, **kwargs)

