
def benchmark_in_sub_process(
    choices: list[TritonTemplateCaller],
) -> dict[TritonTemplateCaller, float]:
    """
    Do benchmarking in a subprocess and return the perf number (latency).
    """
    return get_tuning_process_pool().benchmark(choices)

