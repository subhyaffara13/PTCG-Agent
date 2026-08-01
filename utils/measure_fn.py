
def measure_fn(args, fn, inputs):
    # Measure CPU usage
    pid = os.getpid()
    process = psutil.Process(pid)
    process.cpu_percent(interval=0.1)

    fn(inputs)
    if args.rank == 0:
        logger.info(f"CPU usage: {process.cpu_percent(interval=None) / psutil.cpu_count(logical=False)}%")

    # Measure memory usage
    gc.collect()
    torch.cuda.empty_cache()
    measure_memory(is_gpu=(args.device != "cpu"), func=lambda: fn(inputs))

    # Flush output so memory usage is printed
    sys.stdout.flush()


def measure_fn(args, fn, inputs):
    # Measure CPU usage
    pid = os.getpid()
    process = psutil.Process(pid)
    process.cpu_percent(interval=0.1)

    fn(inputs)
    logger.info(f"CPU usage: {process.cpu_percent(interval=None)}%")

    # Measure memory usage
    gc.collect()
    torch.cuda.empty_cache()
    measure_memory(is_gpu=(args.device != "cpu"), func=lambda: fn(inputs), monitor_type=args.monitor_type)

    # Flush output so memory usage is printed
    sys.stdout.flush()

