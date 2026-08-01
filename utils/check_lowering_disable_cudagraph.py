
def check_lowering_disable_cudagraph(
    device_node_mapping: dict[torch.device, torch.fx.Node],
) -> str | None:
    return check_multiple_devices_or_any_cpu_nodes(device_node_mapping)

