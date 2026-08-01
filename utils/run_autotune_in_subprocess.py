
def run_autotune_in_subprocess(
    benchmark_request: BenchmarkRequest,
) -> float:
    """
    Run autotuning benchmarks in a subprocess.

    This function is submitted to AutotuneProcessPool and runs in isolation
    to prevent GPU contention with the main compilation process.

    Args:
        picklable_choices: List of picklable choice information

    Returns:
        timing
    """

    try:
        # Run the benchmark directly - bmreq is already a BenchmarkRequest
        timing = benchmark_request.benchmark()

        return timing

    except Exception:
        autotuning_log.warning(
            "Failed to benchmark choice %s",
            benchmark_request,
            exc_info=True,
        )
        # Use infinity for failed benchmarks so they're not selected
        return float("inf")

