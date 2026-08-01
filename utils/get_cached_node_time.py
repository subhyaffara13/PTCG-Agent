
def get_cached_node_time(key: str) -> float:
    return get_benchmark_cache().lookup(key)  # type: ignore[return-value]

