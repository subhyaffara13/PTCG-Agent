
def _unsafe_setattr_tensor(module: nn.Module, param_name: str, tensor: Tensor) -> None:
    module._parameters.pop(param_name, None)
    # This bypasses any overrides in case `module` is an instance of an
    # `nn.Module` subclass
    super(nn.Module, module).__setattr__(param_name, tensor)

