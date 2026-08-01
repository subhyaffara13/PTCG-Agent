
def may_ban_benchmarking() -> None:
    if torch._inductor.config.deterministic:
        raise RuntimeError("""In the deterministic mode of Inductor, we will avoid those
        benchmarkings that would cause non deterministic results. Only benchmarkings in the vetted
        scenarios are allowed. Example include autotuning for triton configs of pointwise kernels.

        When you see this exception, you can do one of the following two things:
        1. if the benchmarking you are doing does not introduce any non-determinism, you can just
        add is_vetted_benchmarking=True to you benchmark_gpu call. That would solve the issue.

        2. if the benchmarking you are doing indeed introduces non-determinism, you'll need to disable
        such feature in deterministic mode or find an alternative implementation that is deterministic.
        """)

