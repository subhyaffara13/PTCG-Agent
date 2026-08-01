
def optimize_by_onnxruntime(
    onnx_model: str | ModelProto | None = None,
    use_gpu: bool = False,
    optimized_model_path: str | None = None,
    opt_level: int | None = 99,
    disabled_optimizers: list[str] = [],  # noqa: B006
    verbose: bool = False,
    save_as_external_data: bool = False,
    external_data_filename: str = "",
    external_data_file_threshold: int = 1024,
    *,
    provider: str | None = None,
    **deprecated_kwargs,
) -> str:
    """
    Use onnxruntime to optimize model.

    Args:
        onnx_model (str | ModelProto): the path of input onnx model or ModelProto.
        use_gpu (bool): whether the optimized model is targeted to run in GPU.
        optimized_model_path (str or None): the path of optimized model.
        opt_level (int): graph optimization level.
        disabled_optimizers (List[str]): a list of names of disabled optimizers
        save_as_external_data (bool): whether to save external data outside of ONNX model
        external_data_filename (str): name of external data file. If not provided, name is automatically created from ONNX model.
        external_data_file_threshold (int): threshold to decide whether to save tensor in ONNX model or in external data file
        provider (str or None): execution provider to use if use_gpu
    Returns:
        optimized_model_path (str): the path of optimized model
    """
    assert opt_level in [1, 2, 99]
    from torch import version as torch_version  # noqa: PLC0415

    if onnx_model is None:
        onnx_model = deprecated_kwargs.pop("onnx_model_path", None)
    assert onnx_model is not None

    if (
        use_gpu
        and provider is None
        and set(onnxruntime.get_available_providers()).isdisjoint(
            ["CUDAExecutionProvider", "MIGraphXExecutionProvider"]
        )
    ):
        logger.error("There is no gpu for onnxruntime to do optimization.")
        return onnx_model

    model = (
        OnnxModel(load_model(onnx_model, load_external_data=False))
        if isinstance(onnx_model, str)
        else OnnxModel(onnx_model)
    )
    if model.use_float16() and not use_gpu:
        logger.warning(
            "This model uses float16 in the graph, use_gpu=False might cause extra Cast nodes. "
            "Most operators have no float16 implementation in CPU, so Cast nodes are added to compute them in float32. "
            "If the model is intended to use in GPU, please set use_gpu=True. "
            "Otherwise, consider exporting onnx in float32 and optional int8 quantization for better performance. "
        )

    sess_options = onnxruntime.SessionOptions()
    if opt_level == 1:
        sess_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_BASIC
    elif opt_level == 2:
        sess_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_EXTENDED
    elif opt_level == 3:
        sess_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_LAYOUT
    else:
        sess_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL

    if optimized_model_path is None:
        if isinstance(onnx_model, str):
            path_prefix = str(Path(onnx_model).with_suffix(""))  # remove .onnx suffix
        else:
            path_prefix = "optimized_model"
        optimized_model_path = "{}_o{}_{}.onnx".format(path_prefix, opt_level, "gpu" if use_gpu else "cpu")

    sess_options.optimized_model_filepath = optimized_model_path
    if save_as_external_data:
        if len(external_data_filename) == 0:
            # Set external data filename to model_name.onnx.data
            external_data_filename = os.path.basename(optimized_model_path) + ".data"
        sess_options.add_session_config_entry(
            "session.optimized_model_external_initializers_file_name", external_data_filename
        )
        sess_options.add_session_config_entry(
            "session.optimized_model_external_initializers_min_size_in_bytes", str(external_data_file_threshold)
        )

    if verbose:
        print("Using onnxruntime to optimize model - Debug level Set to verbose")
        sess_options.log_severity_level = 0

    kwargs = {}
    if disabled_optimizers:
        kwargs["disabled_optimizers"] = disabled_optimizers

    if not use_gpu:
        providers = ["CPUExecutionProvider"]
    elif provider is not None:
        if provider == "dml":
            providers = ["DmlExecutionProvider"]
        elif provider == "migraphx":
            providers = ["MIGraphXExecutionProvider"]
        elif provider == "cuda":
            providers = ["CUDAExecutionProvider"]
        elif provider == "tensorrt":
            providers = ["TensorrtExecutionProvider", "CUDAExecutionProvider"]
        else:
            providers = ["CUDAExecutionProvider"]

        providers.append("CPUExecutionProvider")
    else:
        providers = []

        if torch_version.hip:
            providers.append("MIGraphXExecutionProvider")
        else:
            providers.append("CUDAExecutionProvider")

    # For large model, extract external data from model and add to session options
    if isinstance(onnx_model, ModelProto):
        if has_external_data(onnx_model):
            raise ValueError(
                "ModelProto has external data not loaded into memory, ORT cannot create session. "
                "Please load external data before calling this function. "
                "See https://onnx.ai/onnx/repo-docs/ExternalData.html for more information."
            )
        external_names, external_values = extract_raw_data_from_model(onnx_model)
        sess_options.add_external_initializers(list(external_names), list(external_values))

    # Inference session is only used to optimize the model.
    onnx_model = onnx_model.SerializeToString() if isinstance(onnx_model, ModelProto) else onnx_model
    onnxruntime.InferenceSession(onnx_model, sess_options, providers=providers, **kwargs)

    assert os.path.exists(optimized_model_path) and os.path.isfile(optimized_model_path)
    logger.debug("Save optimized model by onnxruntime to %s", optimized_model_path)
    return optimized_model_path

