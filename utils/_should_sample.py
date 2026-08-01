
def _should_sample(profile_sampling_rate: float) -> bool:
    """Determine if current request should be sampled based on sampling rate."""
    if profile_sampling_rate >= 1.0:
        return True  # Always sample
    elif profile_sampling_rate <= 0.0:
        return False  # Never sample

    # Use deterministic sampling based on counter for consistent rate
    global _sample_counter
    with _sample_counter_lock:
        _sample_counter += 1
        # Sample based on rate (e.g., 0.1 means sample every 10th request)
        should_sample = (_sample_counter % int(1.0 / profile_sampling_rate)) == 0
        return should_sample

