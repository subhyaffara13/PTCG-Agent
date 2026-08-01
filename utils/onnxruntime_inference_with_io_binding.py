
def onnxruntime_inference_with_io_binding(session, all_inputs, output_names, test_setting):
    results = []
    latency_list = []
    device = "cuda" if test_setting.use_gpu else "cpu"
    for _test_case_id, inputs in enumerate(all_inputs):
        result = session.run(output_names, inputs)
        results.append(result)
        outputs = {}
        for i in range(len(output_names)):
            outputs[output_names[i]] = result[i]

        input_tensors, output_tensors = create_input_output_tensors(inputs, outputs, device)
        io_binding = create_io_binding(session, input_tensors, output_tensors)

        # warm up once
        session.run_with_iobinding(io_binding)

        start_time = timeit.default_timer()
        session.run_with_iobinding(io_binding)
        latency = timeit.default_timer() - start_time
        latency_list.append(latency)

    return results, latency_list

