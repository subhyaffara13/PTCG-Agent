import sys
import time

def time_fn(args, fn, inputs):
    # Warm up
    warmup_range = (
        range(args.warmup_runs)
        if args.benchmark_type in {"ort-msft", "ort-convert-to-onnx"}
        else trange(args.warmup_runs, file=sys.stdout, desc="Warm up")
    )

    if args.verbose:
        outputs = fn(inputs)
        logger.info(outputs)

    input_sync = lambda *kwargs: (  # noqa: E731
        args.io_binding.synchronize_inputs()
        if args.device != "cpu" and args.benchmark_type in {"ort-msft", "ort-convert-to-onnx"}  # ORT synchronize
        else lambda *kwargs: (
            torch.cuda.synchronize()
            if args.device != "cpu" and torch.cuda.is_available()  # PyTorch synchronize
            else lambda *kwargs: None
        )
    )  # no-op function

    output_sync = lambda *kwargs: (  # noqa: E731
        args.io_binding.synchronize_outputs()
        if args.device != "cpu" and args.benchmark_type in {"ort-msft", "ort-convert-to-onnx"}  # ORT synchronize
        else lambda *kwargs: (
            torch.cuda.synchronize()
            if args.device != "cpu" and torch.cuda.is_available()  # PyTorch synchronize
            else lambda *kwargs: None
        )
    )  # no-op function

    for _ in warmup_range:
        input_sync()
        fn(inputs)
        output_sync()

    # Benchmark
    total_time = 0
    bench_range = (
        range(args.num_runs)
        if args.benchmark_type in {"ort-msft", "ort-convert-to-onnx"}
        else trange(args.num_runs, file=sys.stdout, desc="Benchmark")
    )
    for _ in bench_range:
        input_sync()
        start_time = time.time()

        fn(inputs)

        output_sync()
        end_time = time.time()

        total_time += end_time - start_time

    # Newline print after trange in order to print metrics on new lines without progress bar on same line
    if args.benchmark_type not in {"ort-msft", "ort-convert-to-onnx"}:
        logger.info("")

    latency = total_time / args.num_runs
    throughput = args.batch_size / latency

    if args.rank == 0:
        logger.info(f"Batch Size: {args.batch_size}")
        logger.info(f"Sequence Length: {args.sequence_length}")
        logger.info(f"Latency: {latency} s")
        logger.info(f"Throughput: {throughput} tps")
    return


def time_fn(args, fn, inputs):
    warmup_inputs = inputs[0] if type(inputs) is tuple else inputs
    benchmark_inputs = inputs[1] if type(inputs) is tuple else inputs
    torch_device = torch.device(args.target_device)

    # Warm up
    warmup_range = (
        range(args.warmup_runs)
        if args.benchmark_type == "ort"
        else trange(args.warmup_runs, file=sys.stdout, desc="Warm up")
    )

    if args.verbose:
        outputs = fn(warmup_inputs)
        logger.info(outputs)

    for _ in warmup_range:
        fn(warmup_inputs)

    # Benchmark
    if args.device != "cpu":
        torch.cuda.synchronize(torch_device)
    start_time = time.time()

    bench_range = (
        range(args.num_runs)
        if args.benchmark_type == "ort"
        else trange(args.num_runs, file=sys.stdout, desc="Benchmark")
    )
    for _ in bench_range:
        fn(benchmark_inputs)

    if args.device != "cpu":
        torch.cuda.synchronize(torch_device)
    end_time = time.time()

    # Newline print after trange in order to print metrics on new lines without progress bar on same line
    if args.benchmark_type != "ort":
        logger.info("")

    batch_size = 1
    latency = (end_time - start_time) / args.num_runs
    throughput = batch_size / latency

    logger.info(f"Latency: {latency} s")
    logger.info(f"Throughput: {throughput} qps")
    return

