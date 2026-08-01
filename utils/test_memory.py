
def test_memory(args, device) -> dict[str, Any]:
    if len(args.batch_sizes) > 1:
        raise RuntimeError("For memory test, only one batch_size (-b) is allowed.")
    if len(args.sequence_lengths) > 1:
        raise RuntimeError("For memory test, only one sequence_length (-s) is allowed.")
    if len(args.global_lengths) > 1:
        raise RuntimeError("For memory test, only one global_length (-g) is allowed.")

    model_name = args.model
    onnx_model_path = find_onnx_model(model_name) if not args.onnx else args.onnx

    torch.cuda.empty_cache()
    return test_ort_memory(
        device,
        onnx_model_path,
        args.batch_sizes[0],
        args.sequence_lengths[0],
        args.global_lengths[0],
        args.test_times,
        args.num_threads,
    )

