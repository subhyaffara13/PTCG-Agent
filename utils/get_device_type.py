
def get_device_type(
    x: IRNode | OutputSpec | torch.device | None | str,
) -> str | None:
    if isinstance(x, str) or x is None:
        return x
    elif isinstance(x, torch.device):
        return x.type
    elif isinstance(x, (IRNode, OutputSpec)):
        return get_device_type(x.get_device())
    # pyrefly: ignore [bad-argument-type]
    assert_never(f"get_device_type({x}: {type(x).__name__})")

