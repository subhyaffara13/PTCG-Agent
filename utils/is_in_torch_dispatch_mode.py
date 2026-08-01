
def is_in_torch_dispatch_mode(include_infra_modes: bool = True) -> bool:
    return (
        _is_in_torch_dispatch_mode
        if include_infra_modes
        else _is_in_non_infra_torch_dispatch_mode
    )

