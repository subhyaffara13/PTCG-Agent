
def test_from_window(win_params, Nx: int):
    """Verify that `from_window()` handles parameters correctly.

    The window parameterizations are documented in the `get_window` docstring.
    """
    w_sym, fs = get_window(win_params, Nx, fftbins=False), 16.
    w_per = get_window(win_params, Nx, fftbins=True)
    SFT0 = ShortTimeFFT(w_sym, hop=3, fs=fs, fft_mode='twosided',
                        scale_to='psd', phase_shift=1)
    nperseg = len(w_sym)
    noverlap = nperseg - SFT0.hop
    SFT1 = ShortTimeFFT.from_window(win_params, fs, nperseg, noverlap,
                                    symmetric_win=True, fft_mode='twosided',
                                    scale_to='psd', phase_shift=1)
    # periodic window:
    SFT2 = ShortTimeFFT.from_window(win_params, fs, nperseg, noverlap,
                                    symmetric_win=False, fft_mode='twosided',
                                    scale_to='psd', phase_shift=1)
    # Be informative when comparing instances:
    xp_assert_equal(SFT1.win, SFT0.win)
    xp_assert_close(SFT2.win, w_per / np.sqrt(sum(w_per**2) * fs))
    for n_ in ('hop', 'T', 'fft_mode', 'mfft', 'scaling', 'phase_shift'):
        v0, v1, v2 = (getattr(SFT_, n_) for SFT_ in (SFT0, SFT1, SFT2))
        assert v1 == v0, f"SFT1.{n_}={v1} does not equal SFT0.{n_}={v0}"
        assert v2 == v0, f"SFT2.{n_}={v2} does not equal SFT0.{n_}={v0}"

