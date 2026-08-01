
def use_tangent(node: Node) -> bool:
    """
    Whether the fx node uses tangent input.
    """

    return any(
        is_tangent_node(arg)  # type: ignore[operator]
        for arg in get_args_of_node_type(node)
    )

