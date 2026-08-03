import os
from pathlib import Path


def optimize_model(model_path: Path, opt_model_path: Path):
    """
        Generate model that applies graph optimization (constant folding, etc.)
        parameter model_path: path to the original onnx model
        parameter opt_model_path: path to the optimized onnx model
    :return: optimized onnx model
    """
    sess_option = SessionOptions()
    sess_option.optimized_model_filepath = opt_model_path.as_posix()
    sess_option.graph_optimization_level = GraphOptimizationLevel.ORT_ENABLE_BASIC
    kwargs = {}
    # This will rename constant initializer names, disable it to make test pass.
    kwargs["disabled_optimizers"] = ["ConstantSharing"]
    _ = InferenceSession(model_path.as_posix(), sess_option, providers=["CPUExecutionProvider"], **kwargs)


def optimize_model(
    model_path: pathlib.Path,
    output_path: pathlib.Path,
    level: ort.GraphOptimizationLevel = ort.GraphOptimizationLevel.ORT_ENABLE_BASIC,
    log_level: int = 3,
    use_external_initializers: bool = False,
):
    """
    Optimize an ONNX model using ONNX Runtime to the specified level
    :param model_path: Path to ONNX model
    :param output_path: Path to save optimized model to.
    :param level: onnxruntime.GraphOptimizationLevel to use. Default is ORT_ENABLE_BASIC.
    :param log_level: Log level. Defaults to Error (3) so we don't get output about unused initializers being removed.
                      Warning (2) or Info (1) may be desirable in some scenarios.
    :param use_external_initializers: Set flag to write initializers to an external file. Required if model > 2GB.
                                      Requires onnxruntime 1.17+
    """
    so = ort.SessionOptions()
    so.optimized_model_filepath = str(output_path.resolve())
    so.graph_optimization_level = level
    so.log_severity_level = log_level

    # save using external initializers so models > 2 GB are handled
    if use_external_initializers:
        major, minor, rest = ort.__version__.split(".", 3)
        if (int(major), int(minor)) >= (1, 17):
            so.add_session_config_entry("session.optimized_model_external_initializers_file_name", "external_data.pb")
        else:
            raise ValueError(
                "ONNX Runtime 1.17 or higher required to save initializers as external data when optimizing model. "
                f"Current ONNX Runtime version is {ort.__version__}"
            )

    # create session to optimize. this will write the updated model to output_path
    _ = ort.InferenceSession(str(model_path.resolve(strict=True)), so, providers=["CPUExecutionProvider"])


def optimize_model(
    input: str | ModelProto,
    model_type: str = "bert",
    num_heads: int = 0,
    hidden_size: int = 0,
    optimization_options: FusionOptions | None = None,
    opt_level: int | None = None,
    use_gpu: bool = False,
    only_onnxruntime: bool = False,
    verbose: bool = False,
    *,
    provider: str | None = None,
) -> OnnxModel:
    """Optimize Model by OnnxRuntime and/or python fusion logic.

    ONNX Runtime has graph optimizations (https://onnxruntime.ai/docs/performance/model-optimizations/graph-optimizations.html).
    However, the coverage is limited. We also have graph fusions that implemented in Python to improve the coverage.
    They can combined: ONNX Runtime will run first when opt_level > 0, then graph fusions in Python will be applied.

    To use ONNX Runtime only and no Python fusion logic, use only_onnxruntime flag and a positive opt_level like
        optimize_model(input, opt_level=1, use_gpu=False, only_onnxruntime=True)

    When opt_level is None, we will choose default optimization level according to model type.

    When opt_level is 0 and only_onnxruntime is False, only python fusion logic is used and onnxruntime is disabled.

    When opt_level > 1, use_gpu shall set properly
    since the optimized graph might contain operators for GPU or CPU only.

    If your model is intended for GPU inference only (especially float16 or mixed precision model), it is recommended to
    set use_gpu to be True, otherwise the model is not optimized for GPU inference.

    For BERT model, num_heads and hidden_size are optional. For other model types, you need specify these parameters.

    Args:
        input (str | ModelProto): input model path or ModelProto.
        model_type (str, optional): model type - like bert, bert_tf, bert_keras or gpt2. Defaults to 'bert'.
        num_heads (int, optional): number of attention heads. Defaults to 0.
            0 allows detect the parameter from graph automatically.
        hidden_size (int, optional): hidden size. Defaults to 0.
            0 allows detect the parameter from graph automatically.
        optimization_options (FusionOptions, optional): optimization options that turn on/off some fusions.
            Defaults to None.
        opt_level (int, optional): onnxruntime graph optimization level (0, 1, 2 or 99) or None. Defaults to None.
            When the value is None, default value (1 for bert and gpt2, 0 for other model types) will be used.
            When the level > 0, onnxruntime will be used to optimize model first.
        use_gpu (bool, optional): use gpu or not for onnxruntime. Defaults to False.
        only_onnxruntime (bool, optional): only use onnxruntime to optimize model, and no python fusion.
            Defaults to False.
        provider (str, optional): execution provider to use if use_gpu. Defaults to None.

     Returns:
        object of an optimizer class.
    """
    assert opt_level is None or opt_level in [0, 1, 2, 99]

    if model_type not in MODEL_TYPES:
        logger.warning(f"Unsupported model type: {model_type} for optimization, directly return model.")
        return OnnxModel(load_model(input)) if isinstance(input, str) else OnnxModel(input)

    (optimizer_class, _, default_opt_level) = MODEL_TYPES[model_type]

    if opt_level is None:
        opt_level = default_opt_level

    # Disable constant sharing to avoid model proto str mismatch in test. Ideally the optimizer should not
    # affect other fusions. We can update the expected model proto once the ConstantSharing optimizer logic becomes
    # stable.
    disabled_optimizers = ["ConstantSharing"]
    temp_model_path = None
    temp_dir = tempfile.TemporaryDirectory()
    optimized_model_name = "model_o{}_{}.onnx".format(opt_level, "gpu" if use_gpu else "cpu")
    optimized_model_path = os.path.join(temp_dir.name, optimized_model_name)

    # Auto detect if input model has external data
    has_external_data_file = False
    original_model = load_model(input, load_external_data=False) if isinstance(input, str) else input
    if has_external_data(original_model):
        has_external_data_file = True
    del original_model

    if opt_level > 1:
        # Disable some optimizers that might cause failure in symbolic shape inference or attention fusion.
        disabled_optimizers += (
            []
            if only_onnxruntime
            else [
                "MatMulScaleFusion",
                "MatMulAddFusion",
                "MatmulTransposeFusion",
                "GemmActivationFusion",
                "BiasSoftmaxFusion",
            ]
        )
        temp_model_path = optimize_by_onnxruntime(
            input,
            use_gpu=use_gpu,
            provider=provider,
            optimized_model_path=optimized_model_path,
            opt_level=opt_level,
            disabled_optimizers=disabled_optimizers,
            verbose=verbose,
            save_as_external_data=has_external_data_file,
        )
    elif opt_level == 1:
        # basic optimizations (like constant folding and cast elimination) are not specified to execution provider.
        # Note that use_gpu=False might cause extra Cast nodes for float16 model since most operators does not support float16 in CPU.
        # Sometime, use_gpu=True might cause extra memory copy nodes when some operators are supported only in CPU.
        # We might need remove GPU memory copy nodes as preprocess of optimize_by_fusion if they cause no matching in fusion.
        temp_model_path = optimize_by_onnxruntime(
            input,
            use_gpu=use_gpu,
            provider=provider,
            optimized_model_path=optimized_model_path,
            opt_level=1,
            disabled_optimizers=disabled_optimizers,
            verbose=verbose,
            save_as_external_data=has_external_data_file,
        )

    if only_onnxruntime and not temp_model_path:
        logger.warning("Please specify a positive value for opt_level when only_onnxruntime is True")

    if temp_model_path is not None:
        model = load_model(temp_model_path)
    elif isinstance(input, str):
        model = load_model(input)
    else:
        model = input

    if only_onnxruntime:
        optimizer = optimizer_class(model, num_heads, hidden_size)
    else:
        optimizer = optimize_by_fusion(model, model_type, num_heads, hidden_size, optimization_options)

    # remove the temporary directory
    temp_dir.cleanup()

    return optimizer

