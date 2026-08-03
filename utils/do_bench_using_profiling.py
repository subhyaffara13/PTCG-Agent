from typing import Any, Callable

def do_bench_using_profiling(
    fn: Callable[[], Any],
    warmup: int = 25,
    rep: int = 100,
    is_vetted_benchmarking: bool = False,
) -> float:
    # We did't use decorator may_distort_benchmarking_result directly since that
    # requires us to import torch._inductor.runtime.benchmarking into global scope.
    # Importing torch._inductor.runtime.benchmarking will cause cuda initialization
    # (because of calling torch.cuda.available in global scope)
    # which cause failure in vllm when it create child processes. Check log:
    #   https://gist.github.com/shunting314/c194e147bf981e58df095c14874dd65a
    #
    # Another way to solve the issue is to just move do_bench_using_profiling
    # to torch._inductor.runtime.benchmarking and change all the call site.
    # But that's not trivial due to so many call sites in and out of pytorch.

    from torch._inductor.runtime.benchmarking import may_distort_benchmarking_result

    return may_distort_benchmarking_result(_do_bench_using_profiling)(
        fn, warmup, rep, is_vetted_benchmarking
    )

