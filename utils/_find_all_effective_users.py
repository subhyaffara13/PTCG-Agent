
def _find_all_effective_users(node: fx.Node, op_types: OpTypes) -> OrderedSet[fx.Node]:
    """Find all effective users of a node, where view ops extend the lifetime
    of the original node. If a user is a view op, recursively find users of
    the view."""
    effective_users: OrderedSet[fx.Node] = OrderedSet()
    for user in node.users:
        if user.op == "output":
            continue
        effective_users.add(user)
        if op_types.is_view(user):
            effective_users.update(_find_all_effective_users(user, op_types))
    return effective_users

