from typing import Any

def _infer_attribute(
    node: nodes.AssignAttr | nodes.Attribute,
    context: InferenceContext | None = None,
    **kwargs: Any,
) -> Generator[InferenceResult, None, InferenceErrorInfo]:
    """Infer an AssignAttr/Attribute node by using getattr on the associated object."""
    # pylint: disable=import-outside-toplevel
    from astroid.constraint import get_constraints
    from astroid.nodes import ClassDef

    for owner in node.expr.infer(context):
        if isinstance(owner, util.UninferableBase):
            yield owner
            continue

        context = copy_context(context)
        old_boundnode = context.boundnode
        try:
            context.boundnode = owner
            if isinstance(owner, (ClassDef, Instance)):
                frame = owner if isinstance(owner, ClassDef) else owner._proxied
                context.constraints[node.attrname] = get_constraints(node, frame=frame)
            if node.attrname == "argv" and owner.name == "sys":
                # sys.argv will never be inferable during static analysis
                # It's value would be the args passed to the linter itself
                yield util.Uninferable
            else:
                yield from owner.igetattr(node.attrname, context)
        except (
            AttributeInferenceError,
            InferenceError,
            AttributeError,
        ):
            pass
        finally:
            context.boundnode = old_boundnode
    return InferenceErrorInfo(node=node, context=context)

