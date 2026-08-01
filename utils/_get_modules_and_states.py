
def _get_modules_and_states(
    module: nn.Module,
    device: torch.device,
    ignored_params: set[nn.Parameter] | None,
    is_composable_fn: "Callable[[nn.Module], bool] | None" = None,
    get_state_fn: "Callable[[nn.Module], Any] | None" = None,
) -> tuple[
    nn.Module,
    tuple[nn.Module, ...],
    list[nn.Module],
    list[nn.Parameter],
    list[torch.Tensor],
]:
    """
    Get modules tuple, managed modules, params, and buffers for FSDP/replicate initialization.

    Returns:
        Tuple of (arg_module, modules, managed_modules, params, buffers)
    """
    from torch.distributed.utils import _get_root_modules

    arg_module = module
    modules = (
        (module,) if isinstance(module, nn.Module) else tuple(_get_root_modules(module))
    )

    managed_modules = _get_managed_modules(
        modules, ignored_params, is_composable_fn, get_state_fn
    )
    params, buffers = _get_managed_states(managed_modules, ignored_params)

    _move_states_to_device(params, buffers, device)

    return arg_module, modules, managed_modules, params, buffers

