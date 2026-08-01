
def get_all_devices(gm: torch.fx.GraphModule) -> OrderedSet[torch.device]:
    placeholder_nodes = gm.graph.find_nodes(op="placeholder")
    input_devices: OrderedSet[torch.device] = OrderedSet(
        node.meta["val"].device
        for node in placeholder_nodes
        if isinstance(node.meta.get("val"), torch.Tensor)
    )

    out_arg = output_node(gm).args[0]  # type: ignore[union-attr]
    out_args = out_arg if isinstance(out_arg, tuple) else (out_arg,)
    out_devices: OrderedSet[torch.device] = OrderedSet(
        arg.meta["val"].device
        for arg in out_args
        if isinstance(arg, torch.fx.Node)
        and isinstance(arg.meta.get("val"), torch.Tensor)
    )
    return input_devices | out_devices

