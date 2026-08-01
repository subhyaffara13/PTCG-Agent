
def optimize_by_fusion(
    model: ModelProto,
    model_type: str = "bert",
    num_heads: int = 0,
    hidden_size: int = 0,
    optimization_options: FusionOptions | None = None,
) -> OnnxModel:
    """Optimize Model by graph fusion logic.

    Note that ONNXRuntime graph optimizations (like constant folding) will not be applied. So it is better to enable
    constant folding during exporting ONNX model, or run optimize_by_onnxruntime on the model first like optimize_model.

    For BERT model, num_heads and hidden_size are optional. For other model types, you need to specify these parameters.

    Args:
        model (ModelProto): model object
        model_type (str, optional): model type - like bert, bert_tf, bert_keras or gpt2. Defaults to 'bert'.
        num_heads (int, optional): number of attention heads. Defaults to 0.
                                   0 allows detect the parameter from graph automatically.
        hidden_size (int, optional): hidden size. Defaults to 0.
                                     0 allows detect the parameter from graph automatically.
        optimization_options (FusionOptions, optional): optimization options that turn on/off some fusions.
                                                        Defaults to None.

     Returns:
        object of an optimizer class.
    """
    if model_type not in ["bert", "t5", "swin", "unet", "vae", "clip", "sam2", "mmdit"] and (
        num_heads == 0 or hidden_size == 0
    ):
        logger.warning(f"Please specify parameters of num_heads and hidden_size for model_type {model_type}")

    if model_type not in MODEL_TYPES:
        logger.warning(f"Unsupported model type: {model_type} for graph fusion, directly return model.")
        return OnnxModel(model)

    (optimizer_class, producer, _) = MODEL_TYPES[model_type]

    if model.producer_name and producer != model.producer_name:
        logger.warning(
            f'Model producer not matched: Expected "{producer}", Got "{model.producer_name}".'
            "Please specify correct --model_type parameter."
        )

    if optimization_options is None:
        optimization_options = FusionOptions(model_type)

    optimizer = optimizer_class(model, num_heads, hidden_size)

    optimizer.optimize(optimization_options)

    optimizer.topological_sort()

    optimizer.model.producer_name = "onnxruntime.transformers"
    from onnxruntime import __version__ as onnxruntime_version  # noqa: PLC0415

    optimizer.model.producer_version = onnxruntime_version

    return optimizer

