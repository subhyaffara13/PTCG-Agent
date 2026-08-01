
def infer_typing_alias(
    node: nodes.Call, ctx: context.InferenceContext | None = None
) -> Iterator[nodes.ClassDef]:
    """
    Infers the call to _alias function
    Insert ClassDef, with same name as aliased class,
    in mro to simulate _GenericAlias.

    :param node: call node
    :param context: inference context

    # TODO: evaluate if still necessary when Py3.12 is minimum
    """
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
        lineno=assign_name.lineno,
        col_offset=assign_name.col_offset,
        parent=node.parent,
        end_lineno=assign_name.end_lineno,
        end_col_offset=assign_name.end_col_offset,
    )
    if isinstance(res, nodes.ClassDef):
        # Only add `res` as base if it's a `ClassDef`
        # This isn't the case for `typing.Pattern` and `typing.Match`
        class_def.postinit(bases=[res], body=[], decorators=None)

    maybe_type_var = node.args[1]
    if isinstance(maybe_type_var, nodes.Const) and maybe_type_var.value > 0:
        # If typing alias is subscriptable, add `__class_getitem__` to ClassDef
        func_to_add = _extract_single_node(CLASS_GETITEM_TEMPLATE)
        class_def.locals["__class_getitem__"] = [func_to_add]
    else:
        # If not, make sure that `__class_getitem__` access is forbidden.
        # This is an issue in cases where the aliased class implements it,
        # but the typing alias isn't subscriptable. E.g., `typing.ByteString` for PY39+
        _forbid_class_getitem_access(class_def)

    # Avoid re-instantiating this class every time it's seen
    node._explicit_inference = lambda node, context: iter([class_def])
    return iter([class_def])

