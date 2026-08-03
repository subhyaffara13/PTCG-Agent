import json

def create_session(
    model_path,
    use_gpu,
    provider,
    intra_op_num_threads,
    graph_optimization_level=None,
    log_severity=2,
    tuning_results_path=None,
):
    import onnxruntime  # noqa: PLC0415

    onnxruntime.set_default_logger_severity(log_severity)

    if use_gpu and ("CUDAExecutionProvider" not in onnxruntime.get_available_providers()):
        print(
            "Warning: Please install onnxruntime-gpu package instead of onnxruntime, and use a machine with GPU for testing gpu performance."
        )

    if use_gpu:
        if provider == "dml":
            execution_providers = ["DmlExecutionProvider", "CPUExecutionProvider"]
        elif provider == "migraphx":
            execution_providers = [
                "MIGraphXExecutionProvider",
                "CPUExecutionProvider",
            ]
        elif provider == "cuda":
            execution_providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
        elif provider == "tensorrt":
            execution_providers = [
                "TensorrtExecutionProvider",
                "CUDAExecutionProvider",
                "CPUExecutionProvider",
            ]
        else:
            execution_providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
    else:
        execution_providers = ["CPUExecutionProvider"]

    sess_options = onnxruntime.SessionOptions()
    sess_options.log_severity_level = log_severity
    sess_options.execution_mode = onnxruntime.ExecutionMode.ORT_SEQUENTIAL

    if graph_optimization_level is None:
        sess_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
    elif graph_optimization_level == 0:
        sess_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_DISABLE_ALL
    elif graph_optimization_level == 1:
        sess_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_BASIC
    elif graph_optimization_level == 2:
        sess_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_EXTENDED
    elif graph_optimization_level == 3:
        sess_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_LAYOUT
    elif graph_optimization_level == 99:
        sess_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
    else:
        sess_options.graph_optimization_level = graph_optimization_level

    if intra_op_num_threads is not None:
        sess_options.intra_op_num_threads = intra_op_num_threads

    session = onnxruntime.InferenceSession(model_path, sess_options, providers=execution_providers)

    if use_gpu:
        if provider == "dml":
            assert "DmlExecutionProvider" in session.get_providers()
        elif provider == "migraphx":
            assert "MIGraphXExecutionProvider" in session.get_providers()
        elif provider == "cuda":
            assert "CUDAExecutionProvider" in session.get_providers()
        elif provider == "tensorrt":
            assert "TensorrtExecutionProvider" in session.get_providers()
            assert "CUDAExecutionProvider" in session.get_providers()
        else:
            assert "CUDAExecutionProvider" in session.get_providers()
    else:
        assert "CPUExecutionProvider" in session.get_providers()

    if tuning_results_path is not None:
        with open(tuning_results_path) as f:
            session.set_tuning_results(json.load(f))

    return session


def create_session(config: TestConfig, session_options=None) -> CudaSession:
    ort_session = create_ort_session(config, session_options)
    cuda_session = CudaSession(ort_session, config.device, config.enable_cuda_graph)
    cuda_session.allocate_buffers(config.shape_dict())
    return cuda_session


def create_session(
    onnx_path: str,
    session_options=None,
    provider="CUDAExecutionProvider",
    device: str | torch.device = "cuda",
    enable_cuda_graph=False,
) -> CudaSession:
    ort_session = create_ort_session(
        onnx_path, session_options, provider, enable_cuda_graph=enable_cuda_graph, use_tf32=True
    )
    cuda_session = CudaSession(ort_session, device=torch.device(device), enable_cuda_graph=enable_cuda_graph)
    return cuda_session

