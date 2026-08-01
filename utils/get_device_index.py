
def get_device_index(gm: torch.fx.GraphModule) -> int:
    device = next(iter(get_device_node_mapping(gm)))
    assert device.type == "cuda"
    return device.index

