
def create_ort_session(model_path: str, use_gpu: bool, use_sln_strict_mode: bool) -> InferenceSession:
    """Create OnnxRuntime session.

    Args:
        model_path (str): onnx model path
        use_gpu (bool): use GPU or not
        use_sln_strict_mode (bool): use strict mode for skip layer normalization or not

    Raises:
        RuntimeError: CUDAExecutionProvider is not available when --use_gpu is specified.

    Returns:
        onnxruntime.InferenceSession: The created session.
    """
    sess_options = SessionOptions()
    sess_options.graph_optimization_level = GraphOptimizationLevel.ORT_DISABLE_ALL
    execution_providers = ["CUDAExecutionProvider", "CPUExecutionProvider"] if use_gpu else ["CPUExecutionProvider"]
    if use_gpu:
        if "CUDAExecutionProvider" not in get_available_providers():
            raise RuntimeError("CUDAExecutionProvider is not available for --use_gpu!")
        else:
            logger.info("use CUDAExecutionProvider")
        if use_sln_strict_mode:
            cuda_provider_options = {"enable_skip_layer_norm_strict_mode": True}
            provider_options = {"CUDAExecutionProvider": cuda_provider_options}
            execution_providers = [
                (name, provider_options[name]) if name in provider_options else name for name in execution_providers
            ]

    ort_session = InferenceSession(model_path, sess_options, providers=execution_providers)
    return ort_session


def create_ort_session(config: TestConfig, session_options=None) -> InferenceSession:
    if config.verbose:
        print(f"create session for {vars(config)}")

    if config.provider == "CUDAExecutionProvider":
        device_id = torch.cuda.current_device() if isinstance(config.device, str) else config.device.index
        provider_options = CudaSession.get_cuda_provider_options(device_id, config.enable_cuda_graph)
        provider_options["use_tf32"] = int(config.use_tf32)
        if config.prefer_nhwc:
            provider_options["prefer_nhwc"] = 1
        providers = [(config.provider, provider_options), "CPUExecutionProvider"]
    else:
        providers = ["CPUExecutionProvider"]

    ort_session = InferenceSession(config.onnx_path, session_options, providers=providers)
    return ort_session


def create_ort_session(
    onnx_path: str,
    session_options=None,
    provider="CUDAExecutionProvider",
    enable_cuda_graph=False,
    use_tf32=True,
) -> InferenceSession:
    if provider == "CUDAExecutionProvider":
        device_id = torch.cuda.current_device()
        provider_options = CudaSession.get_cuda_provider_options(device_id, enable_cuda_graph)
        provider_options["use_tf32"] = int(use_tf32)
        providers = [(provider, provider_options), "CPUExecutionProvider"]
    else:
        providers = ["CPUExecutionProvider"]
    logger.info("Using providers: %s", providers)
    return InferenceSession(onnx_path, session_options, providers=providers)

