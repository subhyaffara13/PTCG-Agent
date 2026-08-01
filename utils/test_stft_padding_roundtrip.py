
def test_stft_padding_roundtrip(window, N: int, nperseg: int, noverlap: int,
                                mfft: int, padding):
    """Test the parameter 'padding' of `stft` with roundtrips.

    The STFT parametrizations were taken from the methods
    `test_roundtrip_padded_FFT`, `test_roundtrip_padded_signal` and
    `test_roundtrip_boundary_extension` from class `TestSTFT` in  file
    ``test_spectral.py``. Note that the ShortTimeFFT does not need the
    concept of "boundary extension".
    """
    x = normal_distribution.rvs(size=N, random_state=2909)  # real signal
    z = x * np.exp(1j * np.pi / 4)  # complex signal

    SFT = ShortTimeFFT.from_window(window, 1, nperseg, noverlap,
                                   fft_mode='twosided', mfft=mfft)
    Sx = SFT.stft(x, padding=padding)
    x1 = SFT.istft(Sx, k1=N)
    xp_assert_close(x1, x.astype(np.complex128),
                    err_msg=f"Failed real roundtrip with '{padding}' padding")

    Sz = SFT.stft(z, padding=padding)
    z1 = SFT.istft(Sz, k1=N)
    xp_assert_close(z1, z, err_msg="Failed complex roundtrip with " +
                    f" '{padding}' padding")

