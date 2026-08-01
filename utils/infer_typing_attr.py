
def infer_typing_attr(
    node: nodes.Subscript, ctx: context.InferenceContext | None = None
) -> Iterator[nodes.ClassDef]:
    """Infer a typing.X[...] subscript."""
    try:
        value = next(node.value.infer())  # type: ignore[union-attr] # value shouldn't be None for Subscript.
    except (InferenceError, StopIteration) as exc:
        raise UseInferenceDefault from exc

    if not value.qname().startswith("typing.") or value.qname() in TYPING_ALIAS:
        # If typing subscript belongs to an alias handle it separately.
        raise UseInferenceDefault

    if (
        PY313_PLUS
        and isinstance(value, nodes.FunctionDef)
        and value.qname() == "typing.Annotated"
    ):
        # typing.Annotated is a FunctionDef on 3.13+
        node._explicit_inference = lambda node, context: iter([value])
        return iter([value])

    if isinstance(value, nodes.ClassDef) and value.qname() in {
        "typing.Generic",
        "typing.Annotated",
        "typing_extensions.Annotated",
    }:
        # typing.Generic and typing.Annotated (PY39) are subscriptable
        # through __class_getitem__. Since astroid can't easily
        # infer the native methods, replace them for an easy inference tip
        func_to_add = _extract_single_node(CLASS_GETITEM_TEMPLATE)
        value.locals["__class_getitem__"] = [func_to_add]
        if (
            isinstance(node.parent, nodes.ClassDef)
            and node in node.parent.bases
            and getattr(node.parent, "__cache", None)
        ):
            # node.parent.slots is evaluated and cached before the inference tip
            # is first applied. Remove the last result to allow a recalculation of slots
            cache = node.parent.__cache  # type: ignore[attr-defined] # Unrecognized getattr
            if cache.get(node.parent.slots) is not None:
                del cache[node.parent.slots]
        # Avoid re-instantiating this class every time it's seen
        node._explicit_inference = lambda node, context: iter([value])
        return iter([value])

    node = extract_node(TYPING_TYPE_TEMPLATE.format(value.qname().split(".")[-1]))
    return node.infer(context=ctx)

