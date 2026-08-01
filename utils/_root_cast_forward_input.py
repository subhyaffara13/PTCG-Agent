
def _root_cast_forward_input(
    state: _FSDPState, module: torch.nn.Module, args, kwargs
) -> tuple[Any, Any]:
    if state._handle:
        force_full_precision = not state._handle._force_full_precision
    else:
        force_full_precision = True

    should_cast_forward_inputs = (
        (module.training or not state._use_full_prec_in_eval) and force_full_precision
    ) and state.mixed_precision.cast_root_forward_inputs

    if should_cast_forward_inputs:
        input_dtype: torch.dtype | None = state.mixed_precision.param_dtype
        args, kwargs = _cast_forward_inputs(input_dtype, *args, **kwargs)

    return args, kwargs

