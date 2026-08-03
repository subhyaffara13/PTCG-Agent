from typing import Callable

def benchmark_node(
    n: fx.Node,
    custom_runtime_estimation: Callable[[fx.Node, int | None], float | None]
    | None = None,
) -> float:
    return benchmark_node_with_cache_key(n, custom_runtime_estimation)[0]

