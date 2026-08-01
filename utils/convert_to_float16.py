
def convert_to_float16(args: argparse.Namespace, old_paths: list[str], rank: int = 0):
    decoder_model_fp16_path = os.path.join(args.output, f"rank_{rank}_{args.model_name}_decoder_model_fp16.onnx")
    decoder_with_past_model_fp16_path = os.path.join(
        args.output, f"rank_{rank}_{args.model_name}_decoder_with_past_model_fp16.onnx"
    )
    decoder_merged_model_fp16_path = os.path.join(
        args.output, f"rank_{rank}_{args.model_name}_decoder_merged_model_fp16.onnx"
    )
    new_paths = [decoder_model_fp16_path, decoder_with_past_model_fp16_path, decoder_merged_model_fp16_path]

    logger.info("Converting to float16...")
    for fp32_path, fp16_path in zip(old_paths, new_paths, strict=False):
        if os.path.exists(fp32_path):
            model = OnnxModel(onnx.load_model(fp32_path, load_external_data=True))
            model.convert_float_to_float16(keep_io_types=False)
            model.save_model_to_file(fp16_path, use_external_data_format=True)
            del model
            logger.info(f"The ONNX model at {fp32_path} has been converted to float16 and saved at {fp16_path}!")
            remove_existing_model(fp32_path)

    logger.info(f"The {args.model_name} ONNX model has been successfully converted to float16!")
    return new_paths

