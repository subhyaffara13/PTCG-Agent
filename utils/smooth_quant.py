
def smooth_quant(
    args: argparse.Namespace,
    decoder_model_fp32_path: str,
    decoder_with_past_model_fp32_path: str,
    decoder_model_int8_path: str,
    decoder_with_past_model_int8_path: str,
):
    from neural_compressor import PostTrainingQuantConfig, set_workspace  # noqa: PLC0415
    from neural_compressor import quantization as intel_quantization  # noqa: PLC0415
    from onnx.external_data_helper import load_external_data_for_model  # noqa: PLC0415
    from quant_kv_dataloader import QuantKVDataLoader  # noqa: PLC0415

    set_workspace(args.nc_workspace)
    quantization_config = PostTrainingQuantConfig(
        calibration_sampling_size=[args.calibration_sampling_size],
        recipes={
            "optypes_to_exclude_output_quant": ["MatMul"],
            "smooth_quant": True,
            "smooth_quant_args": {"alpha": args.smooth_quant_alpha},
        },
        op_type_dict={
            "^((?!(MatMul|Gather|Conv)).)*$": {
                "weight": {"dtype": ["fp32"]},
                "activation": {"dtype": ["fp32"]},
            }
        },
    )

    # Convert decoder_model.onnx to INT8
    decoder_model_int8 = intel_quantization.fit(
        decoder_model_fp32_path,
        quantization_config,
        calib_dataloader=QuantKVDataLoader(args),
    )
    load_external_data_for_model(
        decoder_model_int8._model,
        os.path.split(decoder_model_int8._model_path)[0],
    )
    save_onnx_model(
        decoder_model_int8._model,
        decoder_model_int8_path,
        f"{args.model_name}_decoder_model_int8.onnx.data",
    )
    del decoder_model_int8
    logger.info(
        f"The ONNX model at {decoder_model_fp32_path} has been quantized to int8 and saved at {decoder_model_int8_path}!"
    )
    remove_existing_model(decoder_model_fp32_path)

    # Convert decoder_with_past_model.onnx to INT8
    decoder_with_past_model_int8 = intel_quantization.fit(
        decoder_with_past_model_fp32_path,
        quantization_config,
        calib_dataloader=QuantKVDataLoader(args, onnx_model_path=decoder_model_fp32_path),
    )
    load_external_data_for_model(
        decoder_with_past_model_int8._model,
        os.path.split(decoder_with_past_model_int8._model_path)[0],
    )
    save_onnx_model(
        decoder_with_past_model_int8._model,
        decoder_with_past_model_int8_path,
        f"{args.model_name}_decoder_with_past_model_int8.onnx.data",
    )
    del decoder_with_past_model_int8
    logger.info(
        f"The ONNX model at {decoder_with_past_model_fp32_path} has been quantized to int8 and saved at {decoder_with_past_model_int8_path}!"
    )
    remove_existing_model(decoder_with_past_model_fp32_path)

    logger.info(f"The {args.model_name} ONNX model has been successfully quantized to int8!")

    logger.warning(f"Removing {args.nc_workspace}")
    shutil.rmtree(args.nc_workspace)

