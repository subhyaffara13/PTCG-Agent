
def _reset_flat_param_grad_info_if_needed(
    handles: list[FlatParamHandle],
):
    """
    Clears the original parameters' gradients if needed. This method's CPU
    overhead is minimal, so we may call it throughout FSDP methods, which serve
    as callsites to free the gradient memory earlier.
    """
    if not isinstance(handles, list):
        handles = [handles]
    for handle in handles:
        if handle._use_orig_params:
            handle._reset_flat_param_grad_info_if_needed()

