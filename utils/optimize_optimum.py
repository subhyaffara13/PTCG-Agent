
def optimize_optimum(config: AutoConfig, args: argparse.Namespace):
    tmp_file = os.path.join(args.output, args.model_name + ".tmp.onnx")
    output_file = os.path.join(args.output, args.model_name + ".onnx")
    window_size = -1 if not hasattr(config, "sliding_window") else config.sliding_window
    optimize_export(args, config, args.input, tmp_file, remove_model=False, window_size=window_size)
    logger.info(f"Model successfully optimized to {tmp_file}")
    opt_model = OnnxModel(onnx.load_model(tmp_file, load_external_data=True))
    if args.precision == Precision.FLOAT16:
        opt_model.convert_float_to_float16(keep_io_types=False)
        logger.info("Model successfully fused and quantized to FP16!")
    opt_model.save_model_to_file(output_file, use_external_data_format=True)
    logger.info(f"Output model successfully saved to {output_file}")
    logger.info(f"Removing {tmp_file}")
    remove_existing_model(tmp_file)

