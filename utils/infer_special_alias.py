
def infer_special_alias(
    node: nodes.Call, ctx: context.InferenceContext | None = None
) -> Iterator[nodes.ClassDef]:
    """Infer call to tuple alias as new subscriptable class typing.Tuple."""
    if not (
        isinstance(node.parent, nodes.Assign)
        and len(node.parent.targets) == 1
        and isinstance(node.parent.targets[0], nodes.AssignName)
    ):
        raise UseInferenceDefault
    try:
        res = next(node.args[0].infer(context=ctx))
    except StopIteration as e:
        raise InferenceError(node=node.args[0], context=ctx) from e

    assign_name = node.parent.targets[0]
    class_def = nodes.ClassDef(
        name=assign_name.name,
        parent=node.parent,
        lineno=assign_name.lineno,
        col_offset=assign_name.col_offset,
        end_lineno=assign_name.end_lineno,
        end_col_offset=assign_name.end_col_offset,
    )
    class_def.postinit(bases=[res], body=[], decorators=None)
    func_to_add = _extract_single_node(CLASS_GETITEM_TEMPLATE)
    class_def.locals["__class_getitem__"] = [func_to_add]
    # Avoid re-instantiating this class every time it's seen
    node._explicit_inference = lambda node, context: iter([class_def])
    return iter([class_def])

