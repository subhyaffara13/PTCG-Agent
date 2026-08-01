
def _load_parameter_into_model(model: "PreTrainedModel", param_name: str, tensor: torch.Tensor):
    """Cast a single parameter or buffer `param_name` into the `model`, with value `tensor`."""
    parent, param_type = get_module_from_name(model, param_name)
    if param_type in parent._parameters and not isinstance(tensor, nn.Parameter):
        tensor = nn.Parameter(tensor, requires_grad=tensor.is_floating_point())
    # We need to use setattr here, as we set non-persistent buffers as well with this function (`load_state_dict`
    # does not allow to do it)
    setattr(parent, param_type, tensor)

