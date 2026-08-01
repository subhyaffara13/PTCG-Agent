
def run_dynamo_export(
    args: argparse.Namespace, l_config: AutoConfig, llama: AutoModelForCausalLM, rank: int = 0, world_size: int = 1
):
    from torch._dynamo import config  # noqa: PLC0415

    config.capture_scalar_outputs = True

    # Dummy values for export
    batch_size, sequence_length, past_sequence_length = 2, 8, 3
    device = llama.device if args.model_name == "Llama-2-70b-hf" else torch.device("cpu")

    temp_name = args.model_name.lower().replace("-", "").replace("_", "")
    max_sequence_length = 16384 if "codellama" in temp_name else 4096 if "llama2" in temp_name else 2048

    # Export decoder_with_past_model.onnx
    input_ids, attn_mask, pos_ids, past_kv = get_merged_sample_with_past_kv_inputs(
        l_config,
        device,
        batch_size,
        sequence_length,
        past_sequence_length,
        max_seq_len=max_sequence_length,
        use_fp16=False,
        world_size=world_size,
    )
    temp_dir = tempfile.TemporaryDirectory()
    temp_path = os.path.join(temp_dir.name, "temp.onnx")

    input_names = ["input_ids", "attention_mask", "position_ids"]
    output_names = [
        "logits",
        *list(
            chain.from_iterable((f"present.{i}.key", f"present.{i}.value") for i in range(l_config.num_hidden_layers))
        ),
    ]
    dynamic_axes = get_model_dynamic_axes(input_names, output_names)

    model_args = (input_ids, attn_mask, pos_ids, past_kv)
    model_args, model_kwargs, dynamic_shapes = convert_dynamic_axes_into_dynamic_shapes(
        llama, args=model_args, dynamic_axes=dynamic_axes, prefix_mapping={"present": "past_key_values"}
    )

    with bypass_export_some_errors(patch_transformers=True):
        torch.onnx.export(
            llama,
            (),
            temp_path,
            kwargs=model_kwargs,
            dynamic_shapes=dynamic_shapes,
            dynamo=True,
            verbose=args.verbose,
            optimize=True,
        )

    # Check decoder_with_past_model.onnx and save all external data to one file
    onnx.checker.check_model(temp_path)
    onnx.shape_inference.infer_shapes_path(temp_path)

    output_path = os.path.join(args.output, f"rank_{rank}_{args.model_name}_decoder_with_past_model_fp32.onnx")
    onnx_model = onnx.load_model(temp_path, load_external_data=True)
    save_onnx_model(onnx_model, output_path, f"rank_{rank}_{args.model_name}_decoder_with_past_model_fp32.onnx.data")
    del onnx_model
    temp_dir.cleanup()

    logger.info(f"The {args.model_name} ONNX model has been successfully created with the Dynamo exporter!")

