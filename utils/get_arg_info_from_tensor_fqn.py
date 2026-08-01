
def get_arg_info_from_tensor_fqn(model: nn.Module, tensor_fqn: str) -> dict[str, Any]:
    """
    Uses tensor_fqn to obtain a dict containing module_fqn, module and tensor_name
    """
    # string manip to split tensor_fqn into module_fqn and tensor_name
    # if tensor_fqn is 'weight' then module_fqn and tensor_name are '' and 'weight'
    # if tensor_fqn is 'linear.weight' then module_fqn and tensor_name are 'linear' and 'weight'
    tensor_name = tensor_fqn.rsplit(".", maxsplit=1)[-1]
    module_fqn = tensor_fqn[: -len(tensor_name) - ("." in tensor_fqn)]

    module = fqn_to_module(model, module_fqn)

    return {
        "module_fqn": module_fqn,
        "module": module,
        "tensor_name": tensor_name,
        "tensor_fqn": tensor_fqn,
    }

