import time

def run_inference(args, init_inputs, iter_inputs, model):
    if args.benchmark_type in {"hf-pt-eager", "hf-pt-compile", "hf-ort"}:
        run_hf_inference(args, init_inputs, iter_inputs, model)
    elif args.benchmark_type in {"ort-msft", "ort-convert-to-onnx"}:
        run_ort_inference(args, init_inputs, iter_inputs, model)
    else:
        raise Exception(f"Cannot recognize {args.benchmark_type}")


def run_inference(args, model, runs, inputs, outputs):
    if args.benchmark_type == "pt-compile":
        with torch.no_grad():
            outputs = model(**inputs)

    # Synchronize inputs
    io_binding = None
    if args.benchmark_type in {"pt-eager", "pt-compile"}:
        if args.device != "cpu":
            torch.cuda.synchronize(args.target_device)
    else:
        io_binding = add_io_bindings_as_tensors(model, inputs, outputs, args.use_fp16, args.use_buffer_share)
        io_binding.synchronize_inputs()

    # Run inference
    start = time.perf_counter()
    for _ in range(runs):
        if args.benchmark_type in {"pt-eager", "pt-compile"}:
            with torch.no_grad():
                outputs = model(**inputs)
                if args.device != "cpu":
                    torch.cuda.synchronize(args.target_device)
        else:
            model.run_with_iobinding(io_binding)
            io_binding.synchronize_outputs()

    end = time.perf_counter()
    avg = (end - start) / runs
    return avg, outputs


def run_inference(args, inputs, model):
    if args.benchmark_type in {"hf-pt-eager", "hf-pt-compile", "hf-ort"}:
        run_hf_inference(args, inputs, model)
    elif args.benchmark_type == "ort":
        run_ort_inference(args, inputs, model)
    else:
        raise Exception(f"Cannot recognize {args.benchmark_type}")

