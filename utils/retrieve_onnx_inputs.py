
def retrieve_onnx_inputs(model: nn.Module, sample_inputs: tuple, with_past: bool):
    """
    auto retrieve onnx inputs from torch model as we can't enumlate all possibilities
    for all models
    """
    user_inputs = []

    def hook_for_inputs(_, inputs, kwargs):
        user_inputs.append((inputs, kwargs))
        return user_inputs[0]

    hook_handle = model.register_forward_pre_hook(hook_for_inputs, with_kwargs=True)

    forward_params = inspect.signature(model.forward).parameters
    input_keys = list(forward_params.keys())
    default_values = [forward_params.get(key).default for key in input_keys]
    out = model(sample_inputs[0], attention_mask=sample_inputs[1])
    hook_handle.remove()
    user_inputs = user_inputs[0]
    onnx_inputs = default_values
    for idx, _val in enumerate(user_inputs[0]):
        onnx_inputs[idx] = user_inputs[0][idx]
    for key, value in user_inputs[1].items():
        idx = input_keys.index(key)
        onnx_inputs[idx] = value
    for idx, (key, value) in enumerate(zip(input_keys, onnx_inputs, strict=False)):
        if type(value) is torch.Tensor:
            value.to(model.device)
        if "use_cache" in key:
            onnx_inputs[idx] = with_past
            out = model(sample_inputs[0], attention_mask=sample_inputs[1], use_cache=with_past) if with_past else out

    return input_keys, onnx_inputs, out.past_key_values

