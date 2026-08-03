from typing import Any

def _localize_dtensor(
    module: nn.Module, *_: Any, ignored_params: set[nn.Parameter] | None = None
):
    """
    Convert DTensor parameters to local tensors
    """
    if ignored_params is None:
        ignored_params = set()
    param_list = []
    for name, param in module.named_parameters():
        if param in ignored_params:
            continue
        t, sharding_info = _flatten_tensor(param)
        if sharding_info is not None:
            t = nn.Parameter(t)
            t._st_info = sharding_info  # type: ignore[attr-defined]
            param_list.append((*_get_submodule_n_params(module, name), t))
    _update_module_param(param_list)  # type: ignore[arg-type]

