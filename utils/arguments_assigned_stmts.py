from typing import Any

def arguments_assigned_stmts(
    self: nodes.Arguments,
    node: node_classes.AssignedStmtsPossibleNode = None,
    context: InferenceContext | None = None,
    assign_path: list[int] | None = None,
) -> Any:
    from astroid import arguments  # pylint: disable=import-outside-toplevel

    try:
        node_name = node.name  # type: ignore[union-attr]
    except AttributeError:
        # Added to handle edge cases where node.name is not defined.
        # https://github.com/pylint-dev/astroid/pull/1644#discussion_r901545816
        node_name = None  # pragma: no cover

    if context and context.callcontext:
        callee = context.callcontext.callee
        while hasattr(callee, "_proxied"):
            callee = callee._proxied
    else:
        return _arguments_infer_argname(self, node_name, context)
    if node and getattr(callee, "name", None) == node.frame().name:
        # reset call context/name
        callcontext = context.callcontext
        context = copy_context(context)
        context.callcontext = None
        args = arguments.CallSite(callcontext, context=context)
        return args.infer_argument(self.parent, node_name, context)
    return _arguments_infer_argname(self, node_name, context)

