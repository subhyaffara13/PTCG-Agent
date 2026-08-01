
def infer_typing_namedtuple(
    node: nodes.Call, context: InferenceContext | None = None
) -> Iterator[nodes.ClassDef]:
    """Infer a typing.NamedTuple(...) call."""
    # This is essentially a namedtuple with different arguments
    # so we extract the args and infer a named tuple.
    try:
        func = next(node.func.infer())
    except (InferenceError, StopIteration) as exc:
        raise UseInferenceDefault from exc

    if func.qname() not in TYPING_NAMEDTUPLE_QUALIFIED:
        raise UseInferenceDefault

    if len(node.args) != 2:
        raise UseInferenceDefault

    if not isinstance(node.args[1], (nodes.List, nodes.Tuple)):
        raise UseInferenceDefault

    return infer_named_tuple(node, context)

