
def _differential_entropy_is_too_small(samples, kwargs, axis=-1):
    values = samples[0]
    n = values.shape[axis]
    window_length = kwargs.get("window_length")
    if window_length is None:
        window_length = math.floor(math.sqrt(n) + 0.5)
    if not 2 <= 2 * window_length < n:
        return True
    return False

