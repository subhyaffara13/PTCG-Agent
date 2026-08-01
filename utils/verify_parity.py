
def verify_parity(
    args: argparse.Namespace,
    location: str,
    use_auth_token: bool,
    kv_cache_ortvalues: dict,
    pytorch_model: None | torch.nn.Module = None,
    config: None | AutoConfig = None,
):
    # If it's running in a machine where GPU memory < 36GB, it should unload the model in GPU in time and free the GPU memory for ORT.
    py_model = pytorch_model
    if py_model is None:
        config, py_model = setup_torch_model(
            args,
            location,
            use_auth_token,
            torch_dtype=(torch.float16 if args.use_fp16 else torch.float32),
            device=args.device,
        )

    inputs = get_inputs(args, config)

    if "past_key_values" in inputs and pv.Version(transformers_version) >= pv.Version("4.45"):
        # Using DynamicCache
        inputs["past_key_values"] = make_dynamic_cache(inputs["past_key_values"])

    # Run inference with PyTorch
    inputs_after_deepcopy = torch_deepcopy(inputs)
    if args.execution_provider != "cpu":
        torch.cuda.synchronize()
    start_time = time.time()
    # If there is a cache in the inputs, we need to make a copy as the model modifies them inplace.
    # DynamicCache inherits from torch.nn.Module in some version of transformers.
    # We need to make the copy manually.
    pt_outputs = py_model(**inputs_after_deepcopy).logits.detach().cpu().numpy()
    if args.execution_provider != "cpu":
        torch.cuda.synchronize()
    end_time = time.time()
    logger.info(f"PyTorch took {end_time - start_time} s")

    if args.small_gpu and py_model is not None:
        del py_model
        torch.cuda.empty_cache()

    # Run inference with ORT
    past_sequence_length, _, max_sequence_length = get_sequence_lengths(args, config)
    inputs = convert_inputs_for_ort(
        inputs,
        use_buffer_share=args.use_buffer_share,
        past_seq_len=past_sequence_length,
        max_seq_len=max_sequence_length,
    )

    ep = f"{args.execution_provider.upper()}ExecutionProvider"
    if ep == "CUDAExecutionProvider":
        ep = (ep, {"device_id": args.rank})
    ort_model = ort.InferenceSession(
        args.onnx_model_path,
        sess_options=ort.SessionOptions(),
        providers=[ep],
    )
    inputs = verify_ort_inputs(ort_model, inputs)

    # Add IO bindings for non-CPU execution providers
    if args.execution_provider != "cpu":
        io_binding, kv_cache_ortvalues = add_io_bindings_as_ortvalues(
            ort_model,
            ort_inputs=inputs,
            device=args.execution_provider,
            device_id=int(args.rank),
            use_buffer_share=args.use_buffer_share,
            kv_cache_ortvalues=kv_cache_ortvalues,
        )

        io_binding.synchronize_inputs()
        start_time = time.time()
        ort_model.run_with_iobinding(io_binding)
        io_binding.synchronize_outputs()
        end_time = time.time()

        ort_outputs = io_binding.copy_outputs_to_cpu()[0]  # Get logits
        del ort_model

    else:
        start_time = time.time()
        ort_outputs = ort_model.run(None, inputs)
        end_time = time.time()

        ort_outputs = ort_outputs[0]  # Get logits

    logger.info(f"ONNX Runtime took {end_time - start_time} s")

    # Compare PyTorch and ONNX Runtime accuracy
    tol = 2e1 if "int4" in args.onnx_model_path or "int8" in args.onnx_model_path else 5e-1
    parity = np.allclose(pt_outputs, ort_outputs, rtol=tol, atol=tol)
    logger.warning(f"Are PyTorch and ONNX Runtime results close? {parity}")
    if not parity:
        logger.warning(f"Max diff: {np.max(pt_outputs - ort_outputs)}")
    return kv_cache_ortvalues

