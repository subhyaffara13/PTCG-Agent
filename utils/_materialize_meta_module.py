import itertools

def _materialize_meta_module(
    root_module: nn.Module,
    device_from_device_id: torch.device | None,
    ignored_modules: set[nn.Module],
    device_handle: _FSDPDeviceHandle,
):
    # Run default meta device initialization
    materialization_device = device_from_device_id or torch.device(
        device_handle.current_device()
    )
    modules_to_materialize = _get_modules_to_materialize(root_module, ignored_modules)
    module = None
    try:
        # Assume that each module's `reset_parameters()` only initializes its
        # own parameters and not those of its children
        with torch.no_grad():
            for module in modules_to_materialize:
                # As a contract to the user, only call `reset_parameters()` if
                # the module has directly managed parameters/buffers
                module_state_iter = itertools.chain(
                    module.parameters(recurse=False),
                    # pyrefly: ignore [bad-argument-type]
                    module.buffers(recurse=False),
                )
                has_module_states = len(list(module_state_iter)) > 0
                if has_module_states:
                    module.to_empty(device=materialization_device, recurse=False)
                    module.reset_parameters()  # type: ignore[operator]
    except BaseException as e:
        warnings.warn(
            "Unable to call `reset_parameters()` for module on meta "
            f"device with error {str(e)}. Please ensure that your module of"
            f"type {type(module)} implements a `reset_parameters()` method.",
            stacklevel=2,  # type: ignore[possibly-undefined]
        )
        raise e

