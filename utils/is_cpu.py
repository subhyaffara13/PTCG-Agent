
def is_cpu(x: IRNode | torch.device | None | str) -> bool:
    return get_device_type(x) == "cpu"

