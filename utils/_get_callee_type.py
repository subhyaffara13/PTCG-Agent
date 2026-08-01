
def _get_callee_type(call: CallExpr) -> CallableType | None:
    """Return the type of the callee, regardless of its syntactic form."""

    callee_node: Node | None = call.callee

    if isinstance(callee_node, RefExpr):
        callee_node = callee_node.node

    # Some decorators may be using typing.dataclass_transform, which is itself a decorator, so we
    # need to unwrap them to get at the true callee
    if isinstance(callee_node, Decorator):
        callee_node = callee_node.func

    if isinstance(callee_node, (Var, SYMBOL_FUNCBASE_TYPES)) and callee_node.type:
        callee_node_type = get_proper_type(callee_node.type)
        if isinstance(callee_node_type, Overloaded):
            return find_shallow_matching_overload_item(callee_node_type, call)
        elif isinstance(callee_node_type, CallableType):
            return callee_node_type

    return None

