
def inference_ort_with_io_binding(
    ort_session,
    ort_inputs,
    result_template,
    repeat_times,
    ort_output_names,
    ort_outputs,
    output_buffers,
    output_buffer_max_sizes,
    batch_size,
    device,
    data_type=numpy.longlong,
    warm_up_repeat=0,
):
    result = {}

    # Bind inputs and outputs to onnxruntime session
    io_binding = ort_session.io_binding()
    # Bind inputs to device
    for name in ort_inputs:
        np_input = torch.from_numpy(ort_inputs[name]).to(device)
        input_type = IO_BINDING_DATA_TYPE_MAP.get(str(ort_inputs[name].dtype), data_type)
        io_binding.bind_input(
            name,
            np_input.device.type,
            0,
            input_type,
            np_input.shape,
            np_input.data_ptr(),
        )
    # Bind outputs buffers with the sizes needed if not allocated already
    if len(output_buffers) == 0:
        allocateOutputBuffers(output_buffers, output_buffer_max_sizes, device)

    for i, ort_output_name in enumerate(ort_output_names):
        io_binding.bind_output(
            ort_output_name,
            output_buffers[i].device.type,
            0,
            numpy.float32,
            ort_outputs[i].shape,
            output_buffers[i].data_ptr(),
        )

    timeit.repeat(
        lambda: ort_session.run_with_iobinding(io_binding),
        number=1,
        repeat=warm_up_repeat,
    )  # Dry run

    latency_list = timeit.repeat(
        lambda: ort_session.run_with_iobinding(io_binding),
        number=1,
        repeat=repeat_times,
    )
    result.update(result_template)
    result.update({"io_binding": True})
    result.update(get_latency_result(latency_list, batch_size))
    return result

