
def chroma_filter_bank(
    num_frequency_bins: int,
    num_chroma: int,
    sampling_rate: int,
    tuning: float = 0.0,
    power: float | None = 2.0,
    weighting_parameters: tuple[float, float] | None = (5.0, 2.0),
    start_at_c_chroma: bool = True,
):
    """
    Creates a chroma filter bank, i.e a linear transformation to project spectrogram bins onto chroma bins.

    Adapted from *librosa*.

    Args:
        num_frequency_bins (`int`):
            Number of frequencies used to compute the spectrogram (should be the same as in `stft`).
        num_chroma (`int`):
            Number of chroma bins (i.e pitch classes).
        sampling_rate (`float`):
            Sample rate of the audio waveform.
        tuning (`float`):
            Tuning deviation from A440 in fractions of a chroma bin.
        power (`float`, *optional*, defaults to 2.0):
            If 12.0, normalizes each column with their L2 norm. If 1.0, normalizes each column with their L1 norm.
        weighting_parameters (`tuple[float, float]`, *optional*, defaults to `(5., 2.)`):
            If specified, apply a Gaussian weighting parameterized by the first element of the tuple being the center and
            the second element being the Gaussian half-width.
        start_at_c_chroma (`bool`, *optional*, defaults to `True`):
            If True, the filter bank will start at the 'C' pitch class. Otherwise, it will start at 'A'.
    Returns:
        `np.ndarray` of shape `(num_frequency_bins, num_chroma)`
    """
    # Get the FFT bins, not counting the DC component
    frequencies = np.linspace(0, sampling_rate, num_frequency_bins, endpoint=False)[1:]

    freq_bins = num_chroma * hertz_to_octave(frequencies, tuning=tuning, bins_per_octave=num_chroma)

    # make up a value for the 0 Hz bin = 1.5 octaves below bin 1
    # (so chroma is 50% rotated from bin 1, and bin width is broad)
    freq_bins = np.concatenate(([freq_bins[0] - 1.5 * num_chroma], freq_bins))

    bins_width = np.concatenate((np.maximum(freq_bins[1:] - freq_bins[:-1], 1.0), [1]))

    chroma_filters = np.subtract.outer(freq_bins, np.arange(0, num_chroma, dtype="d")).T

    num_chroma2 = np.round(float(num_chroma) / 2)

    # Project into range -num_chroma/2 .. num_chroma/2
    # add on fixed offset of 10*num_chroma to ensure all values passed to
    # rem are positive
    chroma_filters = np.remainder(chroma_filters + num_chroma2 + 10 * num_chroma, num_chroma) - num_chroma2

    # Gaussian bumps - 2*D to make them narrower
    chroma_filters = np.exp(-0.5 * (2 * chroma_filters / np.tile(bins_width, (num_chroma, 1))) ** 2)

    # normalize each column
    if power is not None:
        chroma_filters = chroma_filters / np.sum(chroma_filters**power, axis=0, keepdims=True) ** (1.0 / power)

    # Maybe apply scaling for fft bins
    if weighting_parameters is not None:
        center, half_width = weighting_parameters
        chroma_filters *= np.tile(
            np.exp(-0.5 * (((freq_bins / num_chroma - center) / half_width) ** 2)),
            (num_chroma, 1),
        )

    if start_at_c_chroma:
        chroma_filters = np.roll(chroma_filters, -3 * (num_chroma // 12), axis=0)

    # remove aliasing columns, copy to ensure row-contiguity
    return np.ascontiguousarray(chroma_filters[:, : int(1 + num_frequency_bins / 2)])

