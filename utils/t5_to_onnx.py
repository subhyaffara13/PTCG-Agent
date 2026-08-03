from pathlib import Path


def t5_to_onnx(args: argparse.Namespace):
    """Convert T5 model to onnx

    Args:
        args (argparse.Namespace): arguments parsed from command line
    """
    paths = export_t5_onnx_models(
        model_name_or_path=args.model_name_or_path,
        cache_dir=args.cache_dir,
        output_dir=Path(args.output).parent,
        use_gpu=args.use_gpu,
        use_external_data_format=args.use_external_data_format,
        optimize_onnx=(args.precision != Precision.FLOAT16.value),
        precision=args.precision,
        verbose=False,
        use_decoder_start_token=False,
        overwrite=True,
        disable_auto_mixed_precision=False,
        use_int32_inputs=True,
        model_type=args.model_type,
        encoder_decoder_init=args.encoder_decoder_init,
        force_fp16_io=(args.precision == Precision.FLOAT16.value),  # required by BeamSearch op implementation.
    )

    logger.debug(f"onnx model for encoder: {paths[0]}")
    logger.debug(f"onnx model for decoder: {paths[1]}")
    args.encoder_decoder_init_onnx = paths[0]
    args.decoder_onnx = paths[1]

