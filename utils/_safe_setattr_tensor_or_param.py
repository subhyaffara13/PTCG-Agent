
def _safe_setattr_tensor_or_param(
    module: nn.Module, param_name: str, tensor_or_param: Tensor | nn.Parameter
):
    # Call `delattr()` and `setattr()` to go through `nn.Module` checks
    if hasattr(module, param_name):
        delattr(module, param_name)
    setattr(module, param_name, tensor_or_param)

