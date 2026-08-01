
def _start_profiling_for_request(profile_sampling_rate: float) -> bool:
    """Start profiling for a specific request (if sampling allows)."""
    if _should_sample(profile_sampling_rate):
        _start_profiling(profile_sampling_rate)
        return True
    return False

