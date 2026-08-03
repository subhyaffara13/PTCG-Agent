import os
from pathlib import Path


def export_onnx_model_from_tf(
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
    # Use CPU to export
    import tensorflow as tf  # noqa: PLC0415

    tf.config.set_visible_devices([], "GPU")

    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
    # Fix "Using pad_token, but it is not set yet" error.
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({"pad_token": "[PAD]"})
    max_input_size = tokenizer.model_max_length

    config, model = load_tf_model(model_name, model_class, cache_dir, config_modifier)
    model.resize_token_embeddings(len(tokenizer))

    example_inputs = tokenizer.encode_plus(
        "This is a sample input",
        return_tensors="tf",
        max_length=max_input_size,
        padding="max_length",
        truncation=True,
    )
    example_inputs = filter_inputs(example_inputs, input_names)

    if config.is_encoder_decoder:
        example_inputs["decoder_input_ids"] = tokenizer.encode_plus(
            "This is a sample input",
            return_tensors="tf",
            max_length=max_input_size,
            padding="max_length",
            truncation=True,
        ).input_ids
    if model_name == "unc-nlp/lxmert-base-uncased":
        example_inputs["visual_feats"] = tf.random.normal([1, 1, config.visual_feat_dim])
        example_inputs["visual_pos"] = tf.random.normal([1, 1, config.visual_pos_dim])

    try:
        # Use no past state for these models
        if config.use_cache:
            config.use_cache = False
    except Exception:
        pass

    example_outputs = model(example_inputs, training=False)
    output_names = None

    # For xlnet models, only compare the last_hidden_state output.
    if model_name == "xlnet-base-cased" or model_name == "xlnet-large-cased":
        output_names = ["last_hidden_state"]
        example_outputs = example_outputs["last_hidden_state"]

    # Flatten is needed for gpt2 and distilgpt2. Output name sorting is needed for tf2onnx outputs to match onnx outputs.
    from tensorflow.python.util import nest  # noqa: PLC0415

    example_outputs_flatten = nest.flatten(example_outputs)

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
    tf_internal_model_path = onnx_model_path[:-5] if use_external_data_format else onnx_model_path

    if overwrite or not os.path.exists(tf_internal_model_path):
        logger.info(f"Exporting ONNX model to {onnx_model_path}")
        if not use_external_data_format:
            Path(tf_internal_model_path).parent.mkdir(parents=True, exist_ok=True)

        import zipfile  # noqa: PLC0415

        import tf2onnx  # noqa: PLC0415

        tf2onnx.logging.set_level(tf2onnx.logging.ERROR)
        specs = []
        for name, value in example_inputs.items():
            dims = [None] * len(value.shape)
            specs.append(tf.TensorSpec(tuple(dims), value.dtype, name=name))
        _, _ = tf2onnx.convert.from_keras(
            model,
            input_signature=tuple(specs),
            opset=opset_version,
            large_model=use_external_data_format,
            output_path=tf_internal_model_path,
        )
        if use_external_data_format:
            # need to unpack the zip for run_onnxruntime()
            with zipfile.ZipFile(tf_internal_model_path, "r") as z:
                z.extractall(os.path.dirname(tf_internal_model_path))
            tf_internal_model_path = os.path.join(os.path.dirname(tf_internal_model_path), "__MODEL_PROTO.onnx")
            if os.path.exists(onnx_model_path):
                os.remove(onnx_model_path)
            os.rename(tf_internal_model_path, onnx_model_path)

    else:
        logger.info(f"Skip export since model existed: {onnx_model_path}")

    model_type = model_type + "_tf"
    optimized_onnx_path, is_valid_onnx_model, vocab_size = validate_and_optimize_onnx(
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
        output_names,
        fusion_options,
    )

    return (
        optimized_onnx_path,
        is_valid_onnx_model,
        vocab_size,
        max_input_size,
    )

