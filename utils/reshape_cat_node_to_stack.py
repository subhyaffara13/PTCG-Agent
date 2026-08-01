
def reshape_cat_node_to_stack(
    graph: torch.fx.Graph,
    cat_node: torch.fx.Node,
    stack_node: torch.fx.Node,
    split_or_unbind_dim: int,
) -> None:
    # reshape the cat node to the stack node shape
    stack_shape = stack_node.meta["example_value"].shape
    stack_dim = _get_dim(stack_node)
    if stack_dim != split_or_unbind_dim:
        # case 1: the stack dim is not the same as the split dim
        # we need to reshape the split input before we do the reshape
        reshape_list = list(stack_shape)
        reshape_list[stack_dim], reshape_list[split_or_unbind_dim] = (
            reshape_list[split_or_unbind_dim],
            reshape_list[stack_dim],
        )
        reshape_node = graph.call_function(
            torch.reshape,
            args=(cat_node, tuple(reshape_list)),
        )
        reshape_node.meta["example_value"] = torch.reshape(
            cat_node.meta["example_value"],
            tuple(reshape_list),  # pyrefly: ignore [bad-argument-type]
        )
        permute_list = list(range(len(stack_shape)))
        permute_list[stack_dim], permute_list[split_or_unbind_dim] = (
            permute_list[split_or_unbind_dim],
            permute_list[stack_dim],
        )
        permute_node = graph.call_function(
            torch.permute,
            args=(reshape_node, permute_list),
        )
        permute_node.meta["example_value"] = torch.permute(
            reshape_node.meta["example_value"], permute_list
        )
    else:
        # case 2: the stack dim is the same as the split dim
        # we can directly reshape the split input
        permute_node = cat_node
    reshape_node = graph.call_function(
        torch.Tensor.view,
        args=(permute_node, *stack_shape),  # type: ignore[arg-type]
    )
    stack_node.replace_all_uses_with(reshape_node)
    reshape_node.meta.update(stack_node.meta)
    stack_inputs = stack_node.args[0]  # type: ignore[union-attr]
    # remove stack node
    graph.erase_node(stack_node)
    # check the input of stack node, and remove nodes that have no users
    remove_split_unbind_children(graph, stack_inputs)  # type: ignore[arg-type]

