
def add_io_bindings_as_tensors(
    model: InferenceSession, inputs: dict, outputs: dict, use_fp16: bool, use_buffer_share: bool
):
    # Verify model inputs
    inputs = verify_ort_inputs(model, inputs)

    device = None
    pt_to_np = {
        "torch.int32": np.int32,
        "torch.int64": np.int64,
        "torch.float16": np.float16,
        "torch.float32": np.float32,
    }

    # Bind inputs/outputs to IO binding
    io_binding = model.io_binding()
    for k, v in inputs.items():
        io_binding.bind_input(
            name=k,
            device_type=v.device.type,
            device_id=0 if v.device.type == "cpu" else v.device.index,
            element_type=pt_to_np[repr(v.dtype)],
            shape=tuple(v.shape),
            buffer_ptr=v.data_ptr(),
        )
        device = v.device

    for output in model.get_outputs():
        name = output.name
        # Bind KV cache outputs to KV cache inputs
        v = (
            inputs[name.replace("present", "past_key_values")]
            if use_buffer_share and "present" in name
            else outputs[name]
        )
        io_binding.bind_output(
            name=name,
            device_type=device.type,
            device_id=0 if device.type == "cpu" else device.index,
            element_type=(np.float16 if use_fp16 else np.float32),
            shape=tuple(v.shape),
            buffer_ptr=v.data_ptr(),
        )

    return io_binding

