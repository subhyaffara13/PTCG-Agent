
def _reconstruct_dtensor(module: nn.Module, _input: Any):
    """
    Reconstruct DTensor parameters from local tensors
    """
    param_list = []
    # TODO: To add perf optimizations to this iterations
    for name, t in module.named_parameters():
        if hasattr(t, "_st_info"):
            dtensor = _unflatten_tensor(t, t._st_info)
            param_list.append((*_get_submodule_n_params(module, name), dtensor))
    _update_module_param(param_list)  # type: ignore[arg-type]

