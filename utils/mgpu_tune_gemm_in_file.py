
def mgpu_tune_gemm_in_file(filename_pattern: str, num_gpus: int) -> None:
    r"""Process one or more files and distribute work over one or more GPUs."""
    unique_gemm_entries = _gather_unique_untuned_gemm_from_files(filename_pattern)

    total_gpus = torch.cuda.device_count()

    if not (1 <= num_gpus <= total_gpus):
        raise AssertionError(
            f"num_gpus must be between 1 and {total_gpus}, got {num_gpus}"
        )

    mp_context = mp.get_context("spawn")

    futures = []  # empty list to hold futures

    # GEMM are assigned to GPUs in a round robin manner
    h = 0
    with concurrent.futures.ProcessPoolExecutor(
        max_workers=num_gpus,
        mp_context=mp_context,
        initializer=_check_tuning_assertions,
    ) as executor:
        # The workers are a separate process. TunableOp will be
        # enabled in the child processes if PYTORCH_TUNABLEOP_ENABLED=1
        # In the initializer, we also try to enable TunableOP if th
        # environment variable was NOT set.

        for line in unique_gemm_entries:
            future = executor.submit(_process_single_offline_gemm, line, h)
            futures.append(future)
            h = (h + 1) % num_gpus

        for future in concurrent.futures.as_completed(futures):
            future.result()

    torch.cuda.synchronize()

    _gather_tunableop_results()

