
def lift_lowering_attrs_to_nodes(fx_module: GraphModule) -> None:
    """Recursively traverse all `fx_module` nodes and fetch the module's attributes if the node is a leaf module."""
    submodules = dict(fx_module.named_modules())

    for node in fx_module.graph.nodes:
        if node.op == "call_module":
            if isinstance(submodules[node.target], GraphModule):
                lift_lowering_attrs_to_nodes(submodules[node.target])
            else:
                node.attrs_for_lowering = extract_attrs_for_lowering(
                    submodules[node.target]
                )

