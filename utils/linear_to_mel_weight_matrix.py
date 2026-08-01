
def linear_to_mel_weight_matrix(
    num_mel_bins: int,
    num_spectrogram_bins: int,
    sample_rate: float,
    lower_edge_hertz: float,
    upper_edge_hertz: float,
    dtype,
) -> np.ndarray:
    """NumPy-port of the JAX mel weight matrix logic."""
    # We use float64 for precision, matching the JAX implementation.
    internal_dtype = np.float64

    # HTK excludes the spectrogram DC bin.
    bands_to_zero = 1
    nyquist_hertz = sample_rate / 2.0
    linear_frequencies = np.linspace(0.0, nyquist_hertz, num_spectrogram_bins, dtype=internal_dtype)[bands_to_zero:]
    spectrogram_bins_mel = hertz_to_mel(linear_frequencies, mel_scale="kaldi")[:, np.newaxis]

    edges = np.linspace(
        hertz_to_mel(lower_edge_hertz, mel_scale="kaldi"),
        hertz_to_mel(upper_edge_hertz, mel_scale="kaldi"),
        num_mel_bins + 2,
        dtype=internal_dtype,
    )

    lower_edge_mel, center_mel, upper_edge_mel = (
        edges[:-2][np.newaxis, :],
        edges[1:-1][np.newaxis, :],
        edges[2:][np.newaxis, :],
    )

    lower_slopes = (spectrogram_bins_mel - lower_edge_mel) / (center_mel - lower_edge_mel)
    upper_slopes = (upper_edge_mel - spectrogram_bins_mel) / (upper_edge_mel - center_mel)
    mel_weights_matrix = np.maximum(0.0, np.minimum(lower_slopes, upper_slopes))
    return np.pad(mel_weights_matrix, [[bands_to_zero, 0], [0, 0]]).astype(dtype)

