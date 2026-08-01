
def _get_subgraph_names(
    gm: GraphModule, skip_invoke_subgraph: bool = False
) -> Generator[str, None, None]:
    all_subgraph_names: OrderedSet[str] = OrderedSet(
        x.target for x in gm.graph.find_nodes(op="get_attr")
    )
    fx_subgraph_names: OrderedSet[str] = OrderedSet()
    for child_name, child_module in gm.named_children():
        # Sometimes an owning_module can have unused children. Skip them
        # by checking them from get_attr node targets.
        if child_name in all_subgraph_names and isinstance(
            child_module, torch.fx.GraphModule
        ):
            fx_subgraph_names.add(child_name)

    if skip_invoke_subgraph:
        for node in gm.graph.find_nodes(
            op="call_function", target=torch.ops.higher_order.invoke_subgraph
        ):
            fx_subgraph_names.discard(node.args[0].target)

    yield from fx_subgraph_names

