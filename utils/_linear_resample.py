
def _linear_resample(
    samples: "FloatArray", source_rate: int, target_rate: int
) -> "FloatArray":
    """Linear-interpolation fallback. See :func:`_resample` for caveats."""
    import numpy as np  # type: ignore

    duration = samples.size / float(source_rate)
    target_length = int(round(duration * target_rate))
    if target_length <= 1:
        return samples.astype(np.float32)

    src_indices = np.linspace(0, samples.size - 1, num=target_length, dtype=np.float64)
    left = np.floor(src_indices).astype(np.int64)
    right = np.minimum(left + 1, samples.size - 1)
    frac = (src_indices - left).astype(np.float32)

    return ((1.0 - frac) * samples[left] + frac * samples[right]).astype(np.float32)

