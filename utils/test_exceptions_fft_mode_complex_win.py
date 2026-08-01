
def test_exceptions_fft_mode_complex_win(m: FFT_MODE_TYPE):
    """Verify that one-sided spectra are not allowed with complex-valued
    windows or with complex-valued signals.

    The reason being, the `rfft` function only accepts real-valued input.
    """
    with pytest.raises(ValueError,
                       match=f"One-sided spectra, i.e., fft_mode='{m}'.*"):
        ShortTimeFFT(np.ones(8)*1j, hop=4, fs=1, fft_mode=m)

    SFT = ShortTimeFFT(np.ones(8)*1j, hop=4, fs=1, fft_mode='twosided')
    with pytest.raises(ValueError,
                       match=f"One-sided spectra, i.e., fft_mode='{m}'.*"):
        SFT.fft_mode = m

    SFT = ShortTimeFFT(np.ones(8), hop=4, fs=1, scale_to='psd', fft_mode='onesided')
    with pytest.raises(ValueError, match="Complex-valued `x` not allowed for self.*"):
        SFT.stft(np.ones(8)*1j)
    SFT.fft_mode = 'onesided2X'
    with pytest.raises(ValueError, match="Complex-valued `x` not allowed for self.*"):
        SFT.stft(np.ones(8)*1j)

