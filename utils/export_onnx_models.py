import copy
import os

def export_onnx_models(
    model_name_or_path: str,
    cache_dir: str,
    output_dir: str,
    use_gpu: bool = False,
    use_external_data_format: bool = False,
    optimize_onnx: bool = False,
    precision: str = Precision.FLOAT32.value,
    verbose: bool = False,
    use_decoder_start_token: bool = False,
    overwrite: bool = False,
    disable_auto_mixed_precision: bool = False,
    use_int32_inputs: bool = True,
    model_type: str = "t5",
    state_dict_path: str = "",
    encoder_decoder_init: bool = False,
    force_fp16_io: bool = False,
    shape_infer_before_optimization: bool = False,
):
    assert precision in [Precision.FLOAT32.value, Precision.FLOAT16.value], (
        f"Invalid precision: {precision}. Use 'fp32' or 'fp16'."
    )
    device = torch.device("cuda:0" if use_gpu else "cpu")

    models = T5Helper.load_model(
        model_name_or_path,
        cache_dir,
        device,
        model_type,
        state_dict_path,
        encoder_decoder_init=encoder_decoder_init,
    )
    config: T5Config | MT5Config = models["decoder"].config

    if (not use_external_data_format) and (config.num_layers > 24):
        logger.info("Try use_external_data_format when model size > 2GB")

    output_paths = []
    for name, model in models.items():
        model.to(device)
        filename_suffix = "_" + name

        onnx_path = T5Helper.get_onnx_path(
            output_dir,
            model_name_or_path,
            suffix=filename_suffix,
            new_folder=False,
        )

        if overwrite or not os.path.exists(onnx_path):
            logger.info(f"Exporting ONNX model to {onnx_path}")
            # We have to clone model before exporting onnx, otherwise verify_onnx will report large difference.
            cloned_model = copy.deepcopy(model).to(device)
            T5Helper.export_onnx(
                cloned_model,
                device,
                onnx_path,
                verbose,
                use_external_data_format,
                use_decoder_input_ids=not use_decoder_start_token,
                use_int32_inputs=use_int32_inputs,
            )
        else:
            logger.info(f"Skip exporting: existed ONNX model {onnx_path}")

        # Optimize ONNX graph.
        # The precision shall be compared with string value. It is because the Precision enum loaded from local file
        # (like by transformers test in CI pipeline) are not same as Precision enum from package.
        if optimize_onnx or precision != Precision.FLOAT32.value:
            onnx_shape_path = None
            if shape_infer_before_optimization:
                onnx_shape_path = T5Helper.get_onnx_path(
                    output_dir,
                    model_name_or_path,
                    suffix=filename_suffix + "_shape",
                    new_folder=False,
                )
                infer_shapes_path(onnx_path, onnx_shape_path)

            output_path = T5Helper.get_onnx_path(
                output_dir,
                model_name_or_path,
                suffix=filename_suffix + "_" + str(precision),
                new_folder=False,
            )

            if overwrite or not os.path.exists(output_path):
                logger.info(f"Optimizing model to {output_path}")
                T5Helper.optimize_onnx(
                    onnx_shape_path or onnx_path,
                    output_path,
                    precision == Precision.FLOAT16.value,
                    config.num_heads,
                    config.hidden_size,
                    use_external_data_format,
                    auto_mixed_precision=not disable_auto_mixed_precision,
                    use_gpu=use_gpu,
                    force_fp16_io=force_fp16_io,
                )
            else:
                logger.info(f"Skip optimizing: existed ONNX model {output_path}")
        else:
            output_path = onnx_path

        ort_session = create_onnxruntime_session(
            output_path,
            use_gpu=use_gpu,
            verbose=verbose,
        )
        if ort_session is None:
            break

        with torch.no_grad():
            max_diff = T5Helper.verify_onnx(model, ort_session, device, use_int32_inputs)
        logger.info(f"PyTorch and OnnxRuntime results max difference = {max_diff}")

        # The threshold cannot apply to fp16 model, which need a larger threshold.
        if precision == Precision.FLOAT32.value and max_diff > 1e-4:
            logger.warning("PyTorch and OnnxRuntime results are NOT close")

        output_paths.append(output_path)

    return output_paths


def export_onnx_models(
    model_name_or_path,
    model_impl,
    cache_dir,
    output_dir,
    use_gpu,
    use_external_data_format,
    optimize_onnx,
    precision,
    verbose,
    use_forced_decoder_ids: bool = False,
    merge_encoder_and_decoder_init: bool = True,
    no_beam_search_op: bool = False,
    use_decoder_masked_mha: bool = False,
    output_qk: bool = False,
    overwrite: bool = False,
    use_int32_inputs: bool = True,
    accuracy_level: int = 0,
    quantize_symmetric: bool = False,
    provider: str = "cpu",
    quant_method: str = "k_quant",
):
    device = torch.device("cuda" if use_gpu else "cpu")
    if not use_gpu:
        accuracy_level = 4  # change to 4 for CPU EP
    use_fp16_inputs = precision == Precision.FLOAT16 or (precision in (Precision.INT8, Precision.INT4) and use_gpu)

    models = WhisperHelper.load_model(
        model_name_or_path,
        model_impl,
        cache_dir,
        device,
        torch.float16 if use_fp16_inputs else torch.float32,
        merge_encoder_and_decoder_init,
        no_beam_search_op,
        output_qk,
    )
    config = models["decoder"].config

    if (not use_external_data_format) and (config.num_hidden_layers > 24):
        logger.warning("You MUST pass `--use_external_data_format` because model size > 2GB")
        raise Exception("Please pass `--use_external_data_format` for this model.")

    output_paths = []
    for name, model in models.items():
        print(f"========> Handling {name} model......")
        filename_suffix = "_" + name

        onnx_path = WhisperHelper.get_onnx_path(
            output_dir,
            model_name_or_path,
            suffix=filename_suffix,
            new_folder=False,
        )

        # Export to ONNX
        if overwrite or not os.path.exists(onnx_path):
            logger.info(f"Exporting ONNX model to {onnx_path}")
            WhisperHelper.export_onnx(
                model,
                onnx_path,
                PROVIDERS[provider],
                verbose,
                use_external_data_format,
                use_fp16_inputs=use_fp16_inputs,
                use_int32_inputs=use_int32_inputs,
                use_encoder_hidden_states=(name == "decoder_init"),
                use_kv_cache_inputs=(name == "decoder"),
            )
        else:
            logger.info(f"Skip exporting: existing ONNX model {onnx_path}")

        # Optimize ONNX model
        if optimize_onnx or precision != Precision.FLOAT32:
            output_path = WhisperHelper.get_onnx_path(
                output_dir,
                model_name_or_path,
                suffix=filename_suffix + "_" + str(precision),
                new_folder=False,
            )

            if overwrite or not os.path.exists(output_path):
                if optimize_onnx:
                    logger.info(f"Optimizing model to {output_path}")
                    WhisperHelper.optimize_onnx(
                        onnx_path,
                        output_path,
                        precision == Precision.FLOAT16,
                        model.config.encoder_attention_heads,
                        model.config.d_model,
                        model.config.decoder_layers,
                        use_external_data_format,
                        use_gpu=use_gpu,
                        provider=provider,
                        is_decoder=(name == "decoder"),
                        no_beam_search_op=no_beam_search_op,
                        use_decoder_masked_mha=use_decoder_masked_mha,
                        output_qk=output_qk,
                    )
                    # Remove old ONNX model and old data file
                    if os.path.exists(onnx_path):
                        os.remove(onnx_path)
                    if os.path.exists(onnx_path + ".data"):
                        os.remove(onnx_path + ".data")
                    onnx_path = output_path

                    if isinstance(model, WhisperEncoder):
                        model.verify_onnx(
                            onnx_path,
                            PROVIDERS[provider],
                            use_fp16_inputs=use_fp16_inputs,
                        )
                    else:
                        model.verify_onnx(
                            onnx_path,
                            PROVIDERS[provider],
                            use_fp16_inputs=use_fp16_inputs,
                            use_int32_inputs=use_int32_inputs,
                        )

                if precision in (Precision.INT8, Precision.INT4):
                    onnx_model = onnx.load(onnx_path, load_external_data=True)
                    matmul_nodes = [node.name for node in onnx_model.graph.node if node.op_type == "MatMul"]
                    quant_algo_config = make_quant_algo_config(
                        precision,
                        quant_method,
                        matmul_nodes,
                        encoder_layers=config.encoder_layers,
                        decoder_layers=config.decoder_layers,
                    )

                    quant = MatMulNBitsQuantizer(
                        model=onnx_model,
                        block_size=32,
                        is_symmetric=quantize_symmetric,
                        accuracy_level=accuracy_level,
                        quant_format=QuantFormat.QOperator,
                        op_types_to_quantize=("MatMul",),
                        algo_config=quant_algo_config,
                    )
                    quant.process()
                    if os.path.exists(output_path):
                        os.remove(output_path)
                    if os.path.exists(output_path + ".data"):
                        os.remove(output_path + ".data")
                    onnx.save_model(
                        quant.model.model,
                        output_path,
                        save_as_external_data=True,
                        all_tensors_to_one_file=True,
                        location=os.path.basename(output_path) + ".data",
                        size_threshold=0,
                        convert_attribute=False,
                    )
            else:
                logger.info(f"Skip optimizing: existing ONNX model {onnx_path}")
        else:
            output_path = onnx_path

        output_paths.append(output_path)

    return output_paths

