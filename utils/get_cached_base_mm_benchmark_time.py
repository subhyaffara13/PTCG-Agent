
def get_cached_base_mm_benchmark_time(key: str) -> float:
    return get_pad_cache().lookup(key)  # type: ignore[return-value]

