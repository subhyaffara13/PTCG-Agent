import os
from pathlib import Path


def optimize_onnx_model(
    onnx_model_path,
    optimized_model_path,
    model_type,
    num_attention_heads,
    hidden_size,
    use_gpu,
    precision,
    use_raw_attention_mask,
    overwrite,
    model_fusion_statistics,
    use_external_data_format,
    optimization_options=None,
):
    if overwrite or not os.path.exists(optimized_model_path):
        Path(optimized_model_path).parent.mkdir(parents=True, exist_ok=True)

        from fusion_options import FusionOptions  # noqa: PLC0415
        from optimizer import optimize_model  # noqa: PLC0415

        if optimization_options is None:
            optimization_options = FusionOptions(model_type)
        optimization_options.use_raw_attention_mask(use_raw_attention_mask)
        if precision == Precision.FLOAT16:
            optimization_options.enable_gelu_approximation = True
        if precision == Precision.INT8:
            optimization_options.enable_embed_layer_norm = False

        # For swin models, the num_attention_heads is a list, which isn't supported yet, so set to 0 for now
        if model_type == "swin":
            num_attention_heads = 0
            hidden_size = 0

        # Use script to optimize model.
        # Use opt_level <= 1 for models to be converted to fp16, because some fused op (like FusedGemm) has only fp32 and no fp16.
        # It is better to be conservative so we use opt_level=0 here, in case MemcpyFromHost is added to the graph by OnnxRuntime.
        opt_model = optimize_model(
            onnx_model_path,
            model_type,
            num_heads=num_attention_heads,
            hidden_size=hidden_size,
            opt_level=0,
            optimization_options=optimization_options,
            use_gpu=use_gpu,
            only_onnxruntime=False,
        )
        if model_type == "bert_keras" or model_type == "bert_tf":
            opt_model.use_dynamic_axes()

        model_fusion_statistics[optimized_model_path] = opt_model.get_fused_operator_statistics()

        if precision == Precision.FLOAT16:
            opt_model.convert_float_to_float16(keep_io_types=True)

        opt_model.save_model_to_file(optimized_model_path, use_external_data_format)
    else:
        logger.info(f"Skip optimization since model existed: {optimized_model_path}")

