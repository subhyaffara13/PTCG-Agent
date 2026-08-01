
def maybe_estimate_runtime_benchmark(snode: BaseSchedulerNode) -> float | None:
    bench_fn = None
    args_kwargs_fn = None
    if config.runtime_estimations_mms_benchmark:
        mm_fn = _get_mm_like_fn(snode)
        if mm_fn is None:
            return None
        bench_fn = mm_fn

        args_kwargs_fn = lambda: snode_args_kwargs(snode)  # noqa: E731
    else:
        return None

    cache_key = get_estimate_runtime_cache_key_from_snode(snode)
    cache = get_estimate_runtime_cache()
    cache_val = cache.lookup(cache_key)
    if cache_val is not None:
        assert isinstance(cache_val, float)
        return cache_val

    from .utils import snode_args_kwargs

    args, kwargs = args_kwargs_fn()
    from torch._inductor.runtime.benchmarking import benchmarker

    ms = benchmarker.benchmark(
        bench_fn,
        args,  # pyrefly: ignore[bad-argument-type]
        kwargs,
        memory_warmup_iters=5,
        benchmark_iters=10,
        max_benchmark_duration=10,
    )  # type: ignore[arg-type]

    cache.set_value(cache_key, value=ms)
    return ms

