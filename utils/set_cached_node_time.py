
def set_cached_node_time(key: str, value: float) -> None:
    return get_benchmark_cache().set_value(key, value=value)

