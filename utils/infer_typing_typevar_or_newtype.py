
def infer_typing_typevar_or_newtype(
    node: nodes.Call, context_itton: context.InferenceContext | None = None
) -> Iterator[nodes.ClassDef]:
    """Infer a typing.TypeVar(...) or typing.NewType(...) call."""
    try:
        func = next(node.func.infer(context=context_itton))
    except (InferenceError, StopIteration) as exc:
        raise UseInferenceDefault from exc

    if func.qname() not in TYPING_TYPEVARS_QUALIFIED:
        raise UseInferenceDefault
    if not node.args:
        raise UseInferenceDefault
    # Cannot infer from a dynamic class name (f-string)
    if isinstance(node.args[0], nodes.JoinedStr):
        raise UseInferenceDefault

    typename = node.args[0].as_string().strip("'")
    try:
        node = extract_node(TYPING_TYPE_TEMPLATE.format(typename))
    except AstroidSyntaxError as exc:
        raise InferenceError from exc
    return node.infer(context=context_itton)

