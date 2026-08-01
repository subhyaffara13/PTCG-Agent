
def _get_op_schema(node: Node, placement_strategies: dict[Node, OpSpec]) -> OpSchema:
    """
    Util function to construct the operator schema of a node.
    """
    args_schema_list = pytree.tree_map_only(
        Node, lambda arg: placement_strategies[arg].output_specs, node.args
    )
    op_schema = OpSchema(
        op=cast(torch._ops.OpOverload, node.target),
        args_schema=tuple(args_schema_list),
        kwargs_schema=cast(dict[str, object], node.kwargs),
    )
    return op_schema

