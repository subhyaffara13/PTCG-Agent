
def infer_dict(node: nodes.Call, context: InferenceContext | None = None) -> nodes.Dict:
    """Try to infer a dict call to a Dict node.

    The function treats the following cases:

        * dict()
        * dict(mapping)
        * dict(iterable)
        * dict(iterable, **kwargs)
        * dict(mapping, **kwargs)
        * dict(**kwargs)

    If a case can't be inferred, we'll fallback to default inference.
    """
    call = arguments.CallSite.from_call(node, context=context)
    if call.has_invalid_arguments() or call.has_invalid_keywords():
        raise UseInferenceDefault

    args = call.positional_arguments
    kwargs = list(call.keyword_arguments.items())

    items: list[tuple[InferenceResult, InferenceResult]]
    if not args and not kwargs:
        # dict()
        return nodes.Dict(
            lineno=node.lineno,
            col_offset=node.col_offset,
            parent=node.parent,
            end_lineno=node.end_lineno,
            end_col_offset=node.end_col_offset,
        )
    if kwargs and not args:
        # dict(a=1, b=2, c=4)
        items = [(nodes.Const(key), value) for key, value in kwargs]
    elif len(args) == 1 and kwargs:
        # dict(some_iterable, b=2, c=4)
        elts = _get_elts(args[0], context)
        keys = [(nodes.Const(key), value) for key, value in kwargs]
        items = elts + keys
    elif len(args) == 1:
        items = _get_elts(args[0], context)
    else:
        raise UseInferenceDefault()
    value = nodes.Dict(
        col_offset=node.col_offset,
        lineno=node.lineno,
        parent=node.parent,
        end_lineno=node.end_lineno,
        end_col_offset=node.end_col_offset,
    )
    value.postinit(items)
    return value

