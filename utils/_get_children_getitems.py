
def _get_children_getitems(node: Node) -> Generator[Node, None, None]:
    for user in node.users:
        if user.target is operator.getitem and isinstance(user.args[1], int):
            yield user

