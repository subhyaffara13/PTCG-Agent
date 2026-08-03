import functools
from typing import Any, Callable

def get_do_bench() -> Callable[[Callable[[], Any]], float]:
    return functools.partial(
        # pyrefly: ignore [bad-argument-type]
        torch._inductor.runtime.benchmarking.benchmarker.benchmark_gpu,
        warmup=5,
    )

