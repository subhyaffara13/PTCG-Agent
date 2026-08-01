
def run_profile(onnx_model_path, use_gpu, provider, basic_optimization, thread_num, all_inputs):
    from benchmark_helper import create_onnxruntime_session  # noqa: PLC0415

    session = create_onnxruntime_session(
        onnx_model_path,
        use_gpu,
        provider,
        enable_all_optimization=not basic_optimization,
        num_threads=thread_num,
        enable_profiling=True,
    )

    for inputs in all_inputs:
        _ = session.run(None, inputs)

    profile_file = session.end_profiling()
    return profile_file

