
def autotune_select_algorithm(*args, **kwargs):
    cache = get_algorithm_selector_cache()

    if "return_multi_template" not in kwargs:
        kwargs["return_multi_template"] = (
            torch._inductor.config.benchmark_epilogue_fusion
            or torch._inductor.config.pipeline_max_autotune_gemm
        )

    if "precompilation_timeout_seconds" not in kwargs:
        kwargs["precompilation_timeout_seconds"] = config.precompilation_timeout_seconds

    return cache(*args, **kwargs)

