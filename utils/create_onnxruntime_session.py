
def create_onnxruntime_session(
    onnx_model_path,
    use_gpu,
    provider=None,
    enable_all_optimization=True,
    num_threads=-1,
    enable_profiling=False,
    verbose=False,
    enable_mlas_gemm_fastmath_arm64_bfloat16=False,
    provider_options={},  # map execution provider name to its option  # noqa: B006
):
    sess_options = onnxruntime.SessionOptions()

    if enable_all_optimization:
        sess_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
    else:
        sess_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_BASIC

    if enable_profiling:
        sess_options.enable_profiling = True

    if num_threads > 0:
        sess_options.intra_op_num_threads = num_threads
        logger.debug(f"Session option: intra_op_num_threads={sess_options.intra_op_num_threads}")

    if verbose:
        sess_options.log_severity_level = 0
    else:
        sess_options.log_severity_level = 4

    if provider in onnxruntime.get_available_providers():
        providers = [provider]
    elif use_gpu:
        if provider == "dml":
            providers = ["DmlExecutionProvider", "CPUExecutionProvider"]
        elif provider == "migraphx":
            providers = [
                "MIGraphXExecutionProvider",
                "CPUExecutionProvider",
            ]
        elif provider == "cuda" or provider is None:
            providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
        elif provider == "tensorrt":
            providers = [
                "TensorrtExecutionProvider",
                "CUDAExecutionProvider",
                "CPUExecutionProvider",
            ]
        else:
            raise RuntimeError(f"The execution provider is not supported: {provider}")
    else:
        providers = ["CPUExecutionProvider"]

    if provider_options:
        providers = [(name, provider_options[name]) if name in provider_options else name for name in providers]

    if enable_mlas_gemm_fastmath_arm64_bfloat16:
        sess_options.add_session_config_entry("mlas.enable_gemm_fastmath_arm64_bfloat16", "1")

    session = None
    try:
        session = onnxruntime.InferenceSession(onnx_model_path, sess_options, providers=providers)
    except Exception:
        logger.exception(f"Failed to create session for {onnx_model_path} with providers={providers}")

    return session

