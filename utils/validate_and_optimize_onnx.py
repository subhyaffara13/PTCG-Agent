
def validate_and_optimize_onnx(
    model_name,
    use_external_data_format,
    model_type,
    onnx_dir,
    input_names,
    use_gpu,
    precision,
    optimize_info,
    validate_onnx,
    use_raw_attention_mask,
    overwrite,
    config,
    model_fusion_statistics,
    onnx_model_path,
    example_inputs,
    example_outputs_flatten,
    output_names,
    fusion_options,
):
    is_valid_onnx_model = True
    if validate_onnx:
        is_valid_onnx_model = validate_onnx_model(
            onnx_model_path,
            example_inputs,
            example_outputs_flatten,
            use_gpu,
            False,
            output_names,
        )
    if optimize_info.name == OptimizerInfo.NOOPT.name:
        return onnx_model_path, is_valid_onnx_model, config.vocab_size

    if (
        optimize_info.name == OptimizerInfo.BYSCRIPT.name
        or precision == Precision.FLOAT16
        or precision == Precision.INT8
    ):  # Use script (optimizer.py) to optimize
        optimized_model_path = get_onnx_file_path(
            onnx_dir,
            model_name,
            len(input_names),
            True,
            use_gpu,
            precision,
            False,
            use_external_data_format,
        )
        optimize_onnx_model(
            onnx_model_path,
            optimized_model_path,
            model_type,
            config.num_attention_heads,
            config.hidden_size,
            use_gpu,
            precision,
            use_raw_attention_mask,
            overwrite,
            model_fusion_statistics,
            use_external_data_format,
            fusion_options,
        )

        onnx_model_path = optimized_model_path
        if validate_onnx:
            is_valid_onnx_model = validate_onnx_model(
                onnx_model_path,
                example_inputs,
                example_outputs_flatten,
                use_gpu,
                precision == Precision.FLOAT16,
                output_names,
            )

        if precision == Precision.INT8:
            logger.info(f"Quantizing model: {onnx_model_path}")
            QuantizeHelper.quantize_onnx_model(onnx_model_path, onnx_model_path, use_external_data_format)
            logger.info(f"Finished quantizing model: {onnx_model_path}")

    if optimize_info.name == OptimizerInfo.BYORT.name:  # Use OnnxRuntime to optimize
        if is_valid_onnx_model:
            ort_model_path = add_filename_suffix(onnx_model_path, "_ort")
            optimize_onnx_model_by_ort(
                onnx_model_path,
                ort_model_path,
                use_gpu,
                overwrite,
                model_fusion_statistics,
            )

    return (
        onnx_model_path,
        is_valid_onnx_model,
        config.num_labels if model_type in ["vit", "swin"] else config.vocab_size,
    )

