
def optimize_export(
    args: argparse.Namespace,
    config: AutoConfig,
    input_path: str,
    output_path: str,
    remove_model: bool = True,
    world_size: int = 1,
    window_size: int = -1,
):
    from fusion_options import FusionOptions  # noqa: PLC0415

    optimization_options = FusionOptions("gpt2")

    model_opt = optimize_model(
        input_path,
        model_type="gpt2",
        num_heads=config.num_attention_heads,
        hidden_size=config.hidden_size,
        opt_level=0,
        optimization_options=optimization_options,
        only_onnxruntime=False,
    )
    if args.use_gqa:
        model_opt = use_group_query_attention(config, model_opt, world_size, window_size)
    model_opt.save_model_to_file(output_path, use_external_data_format=True)

    # Run symbolic shape inference on optimized model to avoid shape errors during runtime
    # Ex: Before attention fusion, RotaryEmbedding assumes a 4D input and produces a 4D output.
    # After attention fusion, RotaryEmbedding expects a 3D input and produces a 3D output.
    wheel_cmd = [sys.executable, "-m", "onnxruntime.tools.symbolic_shape_infer"]
    source_cmd = [sys.executable, "../symbolic_shape_infer.py"]
    symbolic_shape_infer_args = [
        "--input",
        output_path,
        "--output",
        output_path,
        "--auto_merge",
        "--save_as_external_data",
        "--all_tensors_to_one_file",
        "--external_data_location",
        os.path.basename(output_path) + ".data",
    ]

    file_path = os.path.dirname(__file__)
    if os.path.exists(os.path.join(file_path, "../../../tools/symbolic_shape_infer.py")):
        main_cmd = wheel_cmd
    else:
        main_cmd = source_cmd
    subprocess.run(main_cmd + symbolic_shape_infer_args)  # noqa: PLW1510

    logger.info(f"The ONNX model at {input_path} has been successfully optimized and saved at {output_path}!")
    if remove_model:
        remove_existing_model(input_path)

