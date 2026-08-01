
def infer_slice(node, context: InferenceContext | None = None):
    """Understand `slice` calls."""
    args = node.args
    if not 0 < len(args) <= 3:
        raise UseInferenceDefault

    infer_func = partial(util.safe_infer, context=context)
    args = [infer_func(arg) for arg in args]
    for arg in args:
        if not arg or isinstance(arg, util.UninferableBase):
            raise UseInferenceDefault
        if not isinstance(arg, nodes.Const):
            raise UseInferenceDefault
        if not isinstance(arg.value, (type(None), int)):
            raise UseInferenceDefault

    if len(args) < 3:
        # Make sure we have 3 arguments.
        args.extend([None] * (3 - len(args)))

    slice_node = nodes.Slice(
        lineno=node.lineno,
        col_offset=node.col_offset,
        parent=node.parent,
        end_lineno=node.end_lineno,
        end_col_offset=node.end_col_offset,
    )
    slice_node.postinit(*args)
    return slice_node

