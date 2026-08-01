
def test_ort_memory(
    device,
    onnx_model_path,
    batch_size,
    sequence_length,
    global_length,
    test_times,
    num_threads,
) -> dict[str, Any]:
    logger.info(
        f"Testing memory for model={onnx_model_path}, batch_size={batch_size}, sequence_length={sequence_length}, "
        f"global_length={global_length}, test_times={test_times}, num_threads={num_threads}"
    )

    def inference():
        # Update Arena strategy so that we can measure the minimum memory required
        cuda_provider_options = {"arena_extend_strategy": "kSameAsRequested"}
        provider_options = {"CUDAExecutionProvider": cuda_provider_options}
        session = benchmark_helper.create_onnxruntime_session(
            onnx_model_path,
            use_gpu=True,
            enable_all_optimization=True,
            num_threads=num_threads,
            provider_options=provider_options,
        )

        dummy_inputs: LongformerInputs = LongformerHelper.get_dummy_inputs(
            batch_size, sequence_length, global_length, device
        )
        ort_inputs = dummy_inputs.get_ort_inputs()
        for _ in range(test_times):
            _ = session.run(None, ort_inputs)

    memory_used = benchmark_helper.measure_memory(is_gpu=True, func=inference)

    return {
        "onnx_model": onnx_model_path,
        "batch_size": batch_size,
        "sequence_length": sequence_length,
        "global_length": global_length,
        "test_times": test_times,
        "num_threads": num_threads,
        "memory": memory_used,
    }

