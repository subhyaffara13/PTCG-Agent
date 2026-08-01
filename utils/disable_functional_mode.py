
def disable_functional_mode() -> Generator[None, None, None]:
    return _disable_infra_mode(torch._C._TorchDispatchModeKey.FUNCTIONAL)

