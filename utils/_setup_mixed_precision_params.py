
def _setup_mixed_precision_params(mixed_precision_config, root_module):
    """Create and free storage for the mixed precision parameters."""
    for param in root_module.parameters():
        # Do not setup mixed precision for DDP ignored parameters.
        if hasattr(param, "_ddp_ignored") and param._ddp_ignored:
            continue

        if not hasattr(param, "_mp_param"):
            param._mp_param = torch.zeros_like(
                param,
                device=param.device,
                dtype=mixed_precision_config.param_dtype,
                requires_grad=param.requires_grad,
            )
            _free_storage(param._mp_param)
            # _fp_param will point to the full precision param so it can be switched
            # back to at the end of forward / backward.
            param._fp_param = param.data

