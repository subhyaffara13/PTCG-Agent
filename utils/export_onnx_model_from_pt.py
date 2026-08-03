import os
from pathlib import Path


def export_onnx_model_from_pt(
    model_name,
    opset_version,
    use_external_data_format,
    model_type,
    model_class,
    config_modifier,
    cache_dir,
    onnx_dir,
    input_names,
    use_gpu,
    precision,
    optimizer_info,
    validate_onnx,
    use_raw_attention_mask,
    overwrite,
    model_fusion_statistics,
    fusion_options,
):
    config, model = load_pt_model(model_name, model_class, cache_dir, config_modifier)
    # config, model = load_pt_model_from_tf(model_name)
    model.cpu()

    example_inputs = None
    max_input_size = None

    if model_type in ["vit", "swin"]:
        image_processor = AutoFeatureExtractor.from_pretrained(model_name, cache_dir=cache_dir)
        data = numpy.random.randint(
            low=0, high=256, size=config.image_size * config.image_size * 3, dtype=numpy.uint8
        ).reshape(config.image_size, config.image_size, 3)

        example_inputs = image_processor(data, return_tensors="pt")
    else:
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        max_input_size = tokenizer.model_max_length
        example_inputs = tokenizer.encode_plus("This is a sample input", return_tensors="pt")

    example_inputs = filter_inputs(example_inputs, input_names)

    example_outputs = model(**example_inputs)

    assert isinstance(example_outputs, (list, tuple)), f"type of output is not list or tuple: {type(example_outputs)}"

    # Flatten is needed for gpt2 and distilgpt2.
    example_outputs_flatten = flatten(example_outputs)
    example_outputs_flatten = update_flatten_list(example_outputs_flatten, [])

    onnx_model_path = get_onnx_file_path(
        onnx_dir,
        model_name,
        len(input_names),
        False,
        use_gpu,
        precision,
        False,
        use_external_data_format,
    )

    if overwrite or not os.path.exists(onnx_model_path):
        logger.info(f"Exporting ONNX model to {onnx_model_path}")
        Path(onnx_model_path).parent.mkdir(parents=True, exist_ok=True)

        dynamic_axes = None
        output_names = None

        if model_type in ["vit", "swin"]:
            dynamic_axes, output_names = {key: {0: "pixel_values"} for key in example_inputs}, ["logits"]
        else:
            dynamic_axes, output_names = build_dynamic_axes(example_inputs, example_outputs_flatten)

        replace_torch_functions()
        torch_onnx_export(
            model=model,
            args=tuple(example_inputs.values()),
            f=onnx_model_path,
            input_names=list(example_inputs.keys()),
            output_names=output_names,
            dynamic_axes=dynamic_axes,
            do_constant_folding=True,
            opset_version=opset_version,
            use_external_data_format=use_external_data_format,
        )
        restore_torch_functions()
    else:
        logger.info(f"Skip export since model existed: {onnx_model_path}")

    onnx_model_file, is_valid_onnx_model, vocab_size = validate_and_optimize_onnx(
        model_name,
        use_external_data_format,
        model_type,
        onnx_dir,
        input_names,
        use_gpu,
        precision,
        optimizer_info,
        validate_onnx,
        use_raw_attention_mask,
        overwrite,
        config,
        model_fusion_statistics,
        onnx_model_path,
        example_inputs,
        example_outputs_flatten,
        None,
        fusion_options,
    )

    return onnx_model_file, is_valid_onnx_model, vocab_size, max_input_size

