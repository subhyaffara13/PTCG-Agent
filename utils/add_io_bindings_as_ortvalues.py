
def add_io_bindings_as_ortvalues(
    model: InferenceSession,
    ort_inputs: dict,
    device: str,
    device_id: int,
    use_buffer_share: bool,
    kv_cache_ortvalues: dict,
):
    io_binding = model.io_binding()

    model_inputs = {i.name for i in model.get_inputs()}
    for k, v in ort_inputs.items():
        # Use this check to handle scenarios such as INT4 CUDA and FP16 CUDA models with
        # GQA + RotaryEmbedding fusion where `position_ids` is removed as an ONNX model input
        # but `position_ids` is used as a PyTorch model input
        if k not in model_inputs:
            continue

        # Bind OrtValue inputs to device
        if use_buffer_share and ("cache" in k or "past_key_values" in k):
            if k not in kv_cache_ortvalues:
                v_device = OrtValue.ortvalue_from_numpy(v, device_type=device, device_id=device_id)
                io_binding.bind_ortvalue_input(k, v_device)
                kv_cache_ortvalues[k] = v_device
            else:
                kv_cache_ortvalues[k].update_inplace(v)
                io_binding.bind_ortvalue_input(k, kv_cache_ortvalues[k])
        else:
            v_device = OrtValue.ortvalue_from_numpy(v, device_type=device, device_id=device_id)
            io_binding.bind_ortvalue_input(k, v_device)

    for output in model.get_outputs():
        name = output.name
        if use_buffer_share and ("out" in name or "present" in name):
            # Bind present KV cache outputs to past KV cache inputs in order to buffer share
            input_name = name.replace("out", "cache").replace("present", "past_key_values")
            io_binding.bind_ortvalue_output(name, kv_cache_ortvalues[input_name])
        else:
            io_binding.bind_output(name, device_type=device, device_id=device_id)

    return io_binding, kv_cache_ortvalues

