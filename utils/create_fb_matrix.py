
def create_fb_matrix(
    n_freqs: int,
    f_min: float,
    f_max: float,
    n_mels: int,
    sample_rate: int,
    fft_length: int,
    norm: str | None = None,
) -> np.ndarray:
    r"""Create a frequency bin conversion matrix (NumPy version).

    Args:
        n_freqs (int): Number of frequencies to highlight/apply
        f_min (float): Minimum frequency (Hz)
        f_max (float): Maximum frequency (Hz)
        n_mels (int): Number of mel filterbanks
        sample_rate (int): Sample rate of the audio waveform
        fft_length (int): FFT length
        norm (Optional[str]): If 'slaney', divide the triangular mel weights by
          the width of the mel band (area normalization). (Default: ``None``)

    Returns:
        np.ndarray: Triangular filter banks (fb matrix) of size (``n_freqs``,
        ``n_mels``)
        meaning number of frequencies to highlight/apply to x the number of
        filterbanks.
        Each column is a filterbank so that assuming there is a matrix A of
        size (..., ``n_freqs``), the applied result would be
        ``A @ create_fb_matrix_numpy(A.shape[-1], ...)``.
    """

    if norm is not None and norm != "slaney":
        raise ValueError("norm must be one of None or 'slaney'")

    # freq bins
    all_freqs = np.arange(n_freqs, dtype=np.float32) * (sample_rate / fft_length)

    # calculate mel freq bins
    # hertz to mel(f) is 2595. * math.log10(1. + (f / 700.))
    m_min = 2595.0 * math.log10(1.0 + (f_min / 700.0))
    m_max = 2595.0 * math.log10(1.0 + (f_max / 700.0))
    m_pts = np.linspace(m_min, m_max, n_mels + 2)
    # mel to hertz(mel) is 700. * (10**(mel / 2595.) - 1.)
    f_pts = 700.0 * (10 ** (m_pts / 2595.0) - 1.0)
    # calculate difference between each mel point and each stft freq point in Hz
    f_diff = f_pts[1:] - f_pts[:-1]  # (n_mels + 1)
    slopes = np.expand_dims(f_pts, 0) - np.expand_dims(all_freqs, 1)  # (n_freqs, n_mels + 2)
    # create overlapping triangles
    zero = np.zeros(1, dtype=np.float32)
    down_slopes = (-1.0 * slopes[:, :-2]) / f_diff[:-1]  # (n_freqs, n_mels)
    up_slopes = slopes[:, 2:] / f_diff[1:]  # (n_freqs, n_mels)
    fb = np.maximum(zero, np.minimum(down_slopes, up_slopes))

    if norm is not None and norm == "slaney":
        # Slaney-style mel is scaled to be approx constant energy per channel
        enorm = 2.0 / (f_pts[2 : n_mels + 2] - f_pts[:n_mels])
        fb *= np.expand_dims(enorm, 0)

    return fb

