
def get_device_node_mapping(
    gm: torch.fx.GraphModule,
) -> dict[torch.device, torch.fx.Node]:
    device_node_mapping: dict[torch.device, torch.fx.Node] = {}
    for n in gm.graph.nodes:
        t = n.meta.get("val", None)
        if isinstance(t, torch.Tensor) and t.device not in device_node_mapping:
            device_node_mapping[t.device] = n
    return device_node_mapping

