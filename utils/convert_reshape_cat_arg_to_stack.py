
def convert_reshape_cat_arg_to_stack(
    graph: torch.fx.Graph,
    cat_node: torch.fx.Node,
    stack_node: torch.fx.Node,
    stack_node_shape: torch.Size,
    stack_dim: int,
    split_dim: int,
) -> torch.fx.Node:
    # reshape the cat node to the stack node shape
    cat_shape = cat_node.meta["example_value"].shape
    if stack_dim != split_dim:
        permute_list = list(range(len(cat_shape)))
        permute_list[stack_dim], permute_list[split_dim] = (
            permute_list[split_dim],
            permute_list[stack_dim],
        )
        permute_node = graph.call_function(
            torch.permute,
            args=(cat_node, permute_list),
        )
        permute_node.meta["example_value"] = torch.permute(
            cat_node.meta["example_value"], permute_list
        )
    else:
        permute_node = cat_node
    reshape_node = graph.call_function(
        torch.Tensor.view,
        args=(permute_node, tuple(stack_node_shape)),  # type: ignore[arg-type]
    )
    reshape_node.meta["example_value"] = torch.Tensor.view(
        permute_node.meta["example_value"],
        tuple(stack_node_shape),  # type: ignore[arg-type]
    )
    return reshape_node

