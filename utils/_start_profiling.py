
def _start_profiling(profile_sampling_rate: float) -> None:
    """Start cProfile profiling once globally."""
    global _profiler
    with _profile_lock:
        if _profiler is None:
            _profiler = cProfile.Profile()
            _profiler.enable()
            verbose_proxy_logger.info(
                f"Profiling started with sampling rate: {profile_sampling_rate}"
            )

