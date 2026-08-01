
def run_torchscript_merged_export(
    args: argparse.Namespace, l_config: AutoConfig, llama: AutoModelForCausalLM, rank: int = 0, world_size: int = 1
):
    # Dummy values for export
    batch_size, sequence_length, past_sequence_length = 2, 8, 0

    # set device used to export model
    # for llama-2-70b we will use current gpus to speed up export process
    # for other models, we will use CPU to make sure we have enough memory to do export
    device = llama.device if args.model_name == "Llama-2-70b-hf" else torch.device("cpu")

    temp_name = args.model_name.lower().replace("-", "").replace("_", "")
    max_sequence_length = 16384 if "codellama" in temp_name else 4096 if "llama2" in temp_name else 2048

    # Export decoder_merged_model.onnx
    decoder_merged_inputs = get_merged_sample_with_past_kv_inputs(
        l_config,
        device,
        batch_size,
        sequence_length,
        past_sequence_length,
        max_seq_len=max_sequence_length,
        use_fp16=False,
        world_size=world_size,
    )
    input_names = [
        "input_ids",
        "attention_mask",
        "position_ids",
        *list(
            chain.from_iterable(
                (f"past_key_values.{i}.key", f"past_key_values.{i}.value") for i in range(l_config.num_hidden_layers)
            )
        ),
    ]
    output_names = [
        "logits",
        *list(
            chain.from_iterable((f"present.{i}.key", f"present.{i}.value") for i in range(l_config.num_hidden_layers))
        ),
    ]
    dynamic_axes = get_merged_model_dynamic_axes(input_names, output_names)

    # Avoid using system temp dir to avoid overflood on hard disk as 70b model is very large.
    # Use temp folder per rank to avoid race condition here.
    temp_dir = f"./temp_{rank}"
    _prepare_dir(temp_dir)
    temp_path = os.path.join(temp_dir, "temp.onnx")

    torch.onnx.export(
        llama,
        args=decoder_merged_inputs,
        f=temp_path,
        export_params=True,
        input_names=input_names,
        output_names=output_names,
        dynamic_axes=dynamic_axes,
        opset_version=torch_export_onnx_opset_version,
        do_constant_folding=True,
        verbose=args.verbose,
        dynamo=False,
    )

    # Check decoder_merged_model.onnx and save all external data to one file
    onnx.checker.check_model(temp_path)
    onnx.shape_inference.infer_shapes_path(temp_path)

    output_path = os.path.join(args.output, f"rank_{rank}_{args.model_name}_decoder_merged_model_fp32.onnx")
    onnx_model = onnx.load_model(temp_path, load_external_data=True)
    save_onnx_model(
        onnx_model,
        output_path,
        f"rank_{rank}_{args.model_name}_decoder_merged_model_fp32.onnx.data",
    )
    del onnx_model
    shutil.rmtree(temp_dir)

    logger.info(f"The {args.model_name} merged ONNX model has been successfully created with the TorchScript exporter!")

