
def benchmark(args, benchmark_cmd, engine):
    log_filename = f"{engine}_{datetime.datetime.now():%Y-%m-%d_%H:%M:%S}.log"
    log_path = os.path.join(args.log_folder, log_filename)
    with open(log_path, "w") as log_file:
        process = subprocess.Popen(benchmark_cmd, stdout=log_file, stderr=log_file)
        try:
            process.wait(args.timeout)
        except subprocess.TimeoutExpired:
            process.kill()

    # Create entries for csv
    logger.info("Gathering data from log files...")
    base_results = [args.warmup_runs, args.num_runs, args.model_name, engine, args.precision, args.device]
    results = process_log_file(args.device_id, log_path, base_results)

    return results


def benchmark(args, benchmark_cmd, engine, audio_file, duration):
    log_filename = f"{engine}_{datetime.datetime.now():%Y-%m-%d_%H:%M:%S}.log"
    log_path = os.path.join(args.log_folder, log_filename)
    with open(log_path, "w") as log_file:
        process = subprocess.Popen(benchmark_cmd, stdout=log_file, stderr=log_file)
        try:
            process.wait(args.timeout)
        except subprocess.TimeoutExpired:
            process.kill()

    # Create entries for csv
    logger.info("Gathering data from log files...")
    base_results = [
        args.warmup_runs,
        args.num_runs,
        args.model_name,
        engine,
        args.precision,
        args.device,
        audio_file,
        duration,
    ]
    results = process_log_file(args.device_id, log_path, base_results)

    return results

