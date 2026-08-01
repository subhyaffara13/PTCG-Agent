
def fetch_onnx_inputs_outputs_name(
    model: nn.Module,
    onnx_inputs: list,
    torch_input_names: tuple,
    past_key_values: tuple,
    with_past: bool,
    input_with_past: bool,
):
    """fetch onnx inputs and outputs name"""
    num_of_past_key = 0
    kv_cache_axis = {0: "batch_size"}
    # try get num_of_past_key and shape of past_key_value
    if past_key_values is not None:
        num_of_past_key = len(past_key_values)
        seq_index = (torch.tensor(past_key_values[0][0].shape) == onnx_inputs[0].shape[-1]).nonzero().view(-1)
        assert seq_index.numel() == 1
        kv_cache_axis = {0: "batch_size", seq_index.item(): "seq_len"}

    if not num_of_past_key:
        num_of_past_key = model.config.num_hidden_layers

    # filter out constant inputs
    onnx_inp_names = tuple(
        [torch_input_names[i] for i in range(len(torch_input_names)) if isinstance(onnx_inputs[i], torch.Tensor)]
    )
    assert "input_ids" in onnx_inp_names and "attention_mask" in onnx_inp_names, (
        "input_ids and attention_mask must be existed in inputs"
    )
    onnx_out_names = ("logits",)
    onnx_dynamic_axes = {
        "input_ids": {0: "batch_size", 1: "seq_len"},
        "attention_mask": {0: "batch_size", 1: "seq_len"},
    }
    # add dyanmic dimensions for the unkonw inputs
    for idx, name in enumerate(onnx_inp_names):
        if name not in onnx_dynamic_axes:
            unknown_dims = {i: f"{idx}__unknown_dims__{i}" for i in range(onnx_inputs[idx].dim())}
            onnx_dynamic_axes[name] = unknown_dims
    if input_with_past:
        for i in range(num_of_past_key):
            onnx_inp_names += (f"past_key_values.{i}.key",)
            onnx_inp_names += (f"past_key_values.{i}.value",)

            onnx_dynamic_axes[onnx_inp_names[-1]] = kv_cache_axis
            onnx_dynamic_axes[onnx_inp_names[-2]] = kv_cache_axis

    if with_past or input_with_past:
        for i in range(num_of_past_key):
            onnx_out_names += (f"present.{i}.key",)
            onnx_out_names += (f"present.{i}.value",)

    for idx, name in enumerate(torch_input_names):
        if input_with_past:
            if name == "past_key_values":
                onnx_inputs[idx] = past_key_values
            elif name == "attention_mask":
                attn_mask = onnx_inputs[idx]
                onnx_inputs[idx] = torch.cat(
                    (attn_mask, torch.ones((attn_mask.shape[0], 1), device=attn_mask.device, dtype=attn_mask.dtype)),
                    dim=1,
                )
            elif name == "input_ids":
                input_ids = onnx_inputs[idx]
                onnx_inputs[idx] = input_ids[:, -1:]

    return onnx_inp_names, onnx_out_names, onnx_dynamic_axes

