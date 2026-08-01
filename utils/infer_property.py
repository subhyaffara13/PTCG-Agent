
def infer_property(
    node: nodes.Call, context: InferenceContext | None = None
) -> objects.Property:
    """Understand `property` class.

    This only infers the output of `property`
    call, not the arguments themselves.
    """
    if len(node.args) < 1:
        # Invalid property call.
        raise UseInferenceDefault

    getter = node.args[0]
    try:
        inferred = next(getter.infer(context=context))
    except (InferenceError, StopIteration) as exc:
        raise UseInferenceDefault from exc

    if not isinstance(inferred, (nodes.FunctionDef, nodes.Lambda)):
        raise UseInferenceDefault

    prop_func = objects.Property(
        function=inferred,
        name="<property>",
        lineno=node.lineno,
        col_offset=node.col_offset,
        # ↓ semantically, the definition of the class of property isn't within
        # node.frame. It's somewhere in the builtins module, but we are special
        # casing it for each "property()" call, so we are making up the
        # definition on the spot, ad-hoc.
        parent=scoped_nodes.SYNTHETIC_ROOT,
    )
    prop_func.postinit(
        body=[],
        args=inferred.args,
        doc_node=getattr(inferred, "doc_node", None),
    )
    return prop_func

