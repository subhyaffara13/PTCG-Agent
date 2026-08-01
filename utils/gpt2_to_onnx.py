
def gpt2_to_onnx(args: argparse.Namespace):
    """Convert GPT-2 model to onnx

    Args:
        args (argparse.Namespace): arguments parsed from command line
    """
    model_name = args.model_name_or_path

    arguments = [
        "--model_name_or_path",
        model_name,
        "--output",
        args.decoder_onnx,
        "--optimize_onnx",
        "--precision",
        args.precision,
        "--test_runs",
        "1",
        "--test_cases",
        "10",
        "--overwrite",  # Overwrite onnx file if existed
    ]
    if args.cache_dir:
        arguments.extend(["--cache_dir", args.cache_dir])
    if args.use_gpu:
        arguments.append("--use_gpu")
    if args.use_external_data_format:
        arguments.append("--use_external_data_format")

    if len(args.op_block_list):
        arguments.extend(["--op_block_list"])
        arguments.extend(args.op_block_list)

    if args.precision == Precision.FLOAT16.value:
        assert args.use_gpu, "fp16 or mixed precision model cannot run in CPU. Please add --use_gpu"
        # TODO(tianleiwu): Use auto mixed precision for fp16 conversion: arguments.append('--auto_mixed_precision')
        #       Need change cuda kernel to support a combination of fp32 logits and fp16 past state.
        #       Currently logits and past state shall be same data type.

    if args.verbose:
        logger.info(f"arguments for convert_to_onnx:{arguments}")

    convert_gpt2_to_onnx(argv=arguments)

