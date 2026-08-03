import functools

def log_lru_cache_stats(wrapped_f: functools._lru_cache_wrapper[object]) -> None:
    log.debug(
        "lru_cache_stats %s: %s",
        wrapped_f.__name__,  # type: ignore[attr-defined]
        wrapped_f.cumulative_cache_info(),  # type: ignore[attr-defined]
    )

