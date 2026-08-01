
def run_onnxruntime(
    use_gpu,
    provider,
    model_names,
    model_class,
    config_modifier,
    precision,
    num_threads,
    batch_sizes,
    sequence_lengths,
    repeat_times,
    input_counts,
    optimizer_info,
    validate_onnx,
    cache_dir,
    onnx_dir,
    verbose,
    overwrite,
    disable_ort_io_binding,
    use_raw_attention_mask,
    model_fusion_statistics,
    model_source,
    enable_arm64_bfloat16_fastmath_mlas_gemm,
    args,
):
    import onnxruntime  # noqa: PLC0415

    results = []
    if (
        use_gpu
        and ("CUDAExecutionProvider" not in onnxruntime.get_available_providers())
        and ("MIGraphXExecutionProvider" not in onnxruntime.get_available_providers())
        and ("DmlExecutionProvider" not in onnxruntime.get_available_providers())
    ):
        logger.error(
            "Please install onnxruntime-gpu or onnxruntime-directml package instead of onnxruntime, and use a machine with GPU for testing gpu performance."
        )
        return results

    warm_up_repeat = 0
    if provider == "tensorrt":
        optimizer_info = OptimizerInfo.NOOPT
        warm_up_repeat = 5
        if "TensorrtExecutionProvider" not in onnxruntime.get_available_providers():
            logger.error(
                "Please install onnxruntime-gpu-tensorrt package, and use a machine with GPU for testing gpu performance."
            )
            return results

    if optimizer_info == OptimizerInfo.NOOPT:
        logger.warning(
            f"OptimizerInfo is set to {optimizer_info}, graph optimizations specified in FusionOptions are not applied."
        )

    for model_name in model_names:
        all_input_names = MODELS[model_name][0]
        for num_inputs in input_counts:
            if num_inputs > len(all_input_names):
                break

            input_names = all_input_names[:num_inputs]
            args.model_type = MODELS[model_name][3]
            fusion_options = FusionOptions.parse(args)

            if "pt" in model_source:
                with torch.no_grad():
                    (
                        onnx_model_file,
                        is_valid_onnx_model,
                        vocab_size,
                        max_sequence_length,
                    ) = export_onnx_model_from_pt(
                        model_name,
                        MODELS[model_name][1],
                        MODELS[model_name][2],
                        MODELS[model_name][3],
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
                    )
            if "tf" in model_source:
                (
                    onnx_model_file,
                    is_valid_onnx_model,
                    vocab_size,
                    max_sequence_length,
                ) = export_onnx_model_from_tf(
                    model_name,
                    MODELS[model_name][1],
                    MODELS[model_name][2],
                    MODELS[model_name][3],
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
                )

            if not is_valid_onnx_model:
                continue

            ort_session = create_onnxruntime_session(
                onnx_model_file,
                use_gpu,
                provider,
                enable_all_optimization=True,
                num_threads=num_threads,
                verbose=verbose,
                enable_mlas_gemm_fastmath_arm64_bfloat16=enable_arm64_bfloat16_fastmath_mlas_gemm,
            )
            if ort_session is None:
                continue

            ort_output_names = [node_arg.name for node_arg in ort_session.get_outputs()]
            output_buffers = []
            device = "cuda" if use_gpu else "cpu"
            config = AutoConfig.from_pretrained(model_name, cache_dir=cache_dir)
            max_last_state_size = numpy.prod(
                [
                    max(batch_sizes),
                    max(sequence_lengths),
                    max(vocab_size, config.hidden_size),
                ]
            )
            max_pooler_size = numpy.prod([max(batch_sizes), config.hidden_size])
            for batch_size in batch_sizes:
                if batch_size <= 0:
                    continue
                for sequence_length in sequence_lengths:
                    if max_sequence_length is not None and sequence_length > max_sequence_length:
                        continue

                    input_value_type = numpy.int64 if "pt" in model_source else numpy.int32
                    ort_inputs = create_onnxruntime_input(
                        vocab_size,
                        batch_size,
                        sequence_length,
                        input_names,
                        config,
                        input_value_type,
                    )
                    result_template = {
                        "engine": "onnxruntime",
                        "version": onnxruntime.__version__,
                        "providers": provider,
                        "device": device,
                        "optimizer": optimizer_info,
                        "precision": precision,
                        "io_binding": not disable_ort_io_binding,
                        "model_name": model_name,
                        "inputs": num_inputs,
                        "threads": num_threads,
                        "batch_size": batch_size,
                        "sequence_length": sequence_length,
                        "custom_layer_num": config_modifier.get_layer_num(),
                        "datetime": str(datetime.now()),
                    }

                    if config.model_type in ["vit", "swin"]:
                        logger.info(
                            f"Run onnxruntime on {model_name} with input shape {[batch_size, 3, config.image_size, config.image_size]}"
                        )
                    else:
                        logger.info(f"Run onnxruntime on {model_name} with input shape {[batch_size, sequence_length]}")

                    if disable_ort_io_binding:
                        result = inference_ort(
                            ort_session,
                            ort_inputs,
                            result_template,
                            repeat_times,
                            batch_size,
                            warm_up_repeat,
                        )
                    else:
                        # Get output sizes from a dummy ort run
                        ort_outputs = ort_session.run(ort_output_names, ort_inputs)
                        output_buffer_max_sizes = [max_last_state_size]
                        for i in range(len(ort_outputs)):
                            if i == 2 and MODELS[model_name][3] == "gpt":
                                # past state output max size
                                output_buffer_max_sizes.append(max_pooler_size)
                            else:
                                output_buffer_max_sizes.append(max_last_state_size)

                        data_type = numpy.longlong if "pt" in model_source else numpy.intc
                        result = inference_ort_with_io_binding(
                            ort_session,
                            ort_inputs,
                            result_template,
                            repeat_times,
                            ort_output_names,
                            ort_outputs,
                            output_buffers,
                            output_buffer_max_sizes,
                            batch_size,
                            device,
                            data_type,
                            warm_up_repeat,
                        )
                    logger.info(result)
                    results.append(result)

    return results

