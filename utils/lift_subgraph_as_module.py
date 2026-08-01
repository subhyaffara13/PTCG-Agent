
def lift_subgraph_as_module(
    gm: GraphModule,
    subgraph: Graph,
    comp_name: str = "",
    class_name: str = "GraphModule",
) -> tuple[GraphModule, dict[str, str]]:
    """
    Create a GraphModule for subgraph, which copies the necessary attributes from the original parent graph_module.

    Args:
        gm (GraphModule): parent graph module

        subgraph (Graph): a valid subgraph that contains copied nodes from the parent graph

        comp_name (str): name for the new component

        class_name (str): name for the submodule

    """

    # Loop through all module calls (call_module) and param fetches (get_attr)
    # in this component, creating HolderModules as necessary to match the path.
    # e.g. if in the original module there's a get_attr node fetches "conv.weight".
    # We create a HolderModule as root -> add a HolderModule named "conv" ->
    # make "weight" a attribute of "conv" HolderModule and point to conv.weight in
    # the original module.
    submodule = HolderModule({})
    orig_to_split_fqn_mapping: dict[str, str] = {}
    for n in subgraph.nodes:
        if n.op not in ("call_module", "get_attr"):
            continue

        target = n.target
        if not isinstance(target, str):
            raise AssertionError(f"Expected str target, got {type(target)}")
        target_name_parts = target.split(".")
        curr = submodule
        orig_gm = gm

        for name in target_name_parts[:-1]:
            if not hasattr(curr, name):
                curr.add_module(name, HolderModule({}))

            curr = getattr(curr, name)
            orig_gm = getattr(orig_gm, name)

        leaf_node_name = target_name_parts[-1]
        leaf_node = getattr(orig_gm, leaf_node_name)

        orig_to_split_fqn_mapping[target] = f"{comp_name}.{target}"
        # Relies on custom __setattr__ magic.
        setattr(curr, leaf_node_name, leaf_node)

    return GraphModule(submodule, subgraph, class_name), orig_to_split_fqn_mapping

