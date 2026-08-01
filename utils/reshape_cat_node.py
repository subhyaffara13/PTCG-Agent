
def reshape_cat_node(
    graph: torch.fx.Graph,
    cat_node: torch.fx.Node,
    unbind_input: torch.fx.Node,
    cat_dim: int,
    unbind_dim: int,
    cat_shape: torch.Size,
) -> torch.fx.Node:
    if cat_dim != unbind_dim:
        # construct the permute node args, which has the same shape as the slice node
        # then it has the same dim as the unbind_input, i.e., shape of cat + 1
        with graph.inserting_after(cat_node):
            permute_list = list(range(len(cat_shape) + 1))
            permute_list[unbind_dim], permute_list[cat_dim] = (
                permute_list[cat_dim],
                permute_list[unbind_dim],
            )
            permute_node = graph.call_function(
                torch.permute,
                args=(unbind_input, permute_list),
            )
            permute_node.meta["example_value"] = torch.permute(
                unbind_input.meta["example_value"], permute_list
            )  # type: ignore[arg-type]
    else:
        permute_node = unbind_input
    with graph.inserting_after(permute_node):
        reshape_node = graph.call_function(
            torch.reshape, args=(permute_node, tuple(cat_shape))
        )
        reshape_node.meta["example_value"] = torch.reshape(
            permute_node.meta["example_value"], tuple(cat_shape)
        )  # type: ignore[arg-type]
    return reshape_node

