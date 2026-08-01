
def amplitude_to_db_batch(
    spectrogram: np.ndarray, reference: float = 1.0, min_value: float = 1e-5, db_range: float | None = None
) -> np.ndarray:
    """
    Converts a batch of amplitude spectrograms to the decibel scale. This computes `20 * log10(spectrogram / reference)`,
    using basic logarithm properties for numerical stability.

    The function supports batch processing, where each item in the batch is an individual amplitude (mel) spectrogram.

    Args:
        spectrogram (`np.ndarray`):
            The input batch of amplitude (mel) spectrograms. Expected shape is (batch_size, *spectrogram_shape).
        reference (`float`, *optional*, defaults to 1.0):
            Sets the input spectrogram value that corresponds to 0 dB. For example, use `np.max(spectrogram)` to set
            the loudest part to 0 dB. Must be greater than zero.
        min_value (`float`, *optional*, defaults to `1e-5`):
            The spectrogram will be clipped to this minimum value before conversion to decibels, to avoid taking
            `log(0)`. The default of `1e-5` corresponds to a minimum of -100 dB. Must be greater than zero.
        db_range (`float`, *optional*):
            Sets the maximum dynamic range in decibels. For example, if `db_range = 80`, the difference between the
            peak value and the smallest value will never be more than 80 dB. Must be greater than zero.

    Returns:
        `np.ndarray`: the batch of spectrograms in decibels
    """
    if reference <= 0.0:
        raise ValueError("reference must be greater than zero")
    if min_value <= 0.0:
        raise ValueError("min_value must be greater than zero")

    reference = max(min_value, reference)

    spectrogram = np.clip(spectrogram, a_min=min_value, a_max=None)
    spectrogram = 20.0 * (np.log10(spectrogram) - np.log10(reference))

    if db_range is not None:
        if db_range <= 0.0:
            raise ValueError("db_range must be greater than zero")
        # Apply db_range clipping per batch item
        max_values = spectrogram.max(axis=(1, 2), keepdims=True)
        spectrogram = np.clip(spectrogram, a_min=max_values - db_range, a_max=None)

    return spectrogram

