
def test_tutorial_stft_legacy_spectrogram():
    """Verify spectrogram example in "Comparison with Legacy Implementation"
    from the "User Guide".

    In :ref:`tutorial_stft_legacy_stft` (file ``signal.rst``) of the
    :ref:`user_guide` the legacy and the new implementation are compared.
    """
    fs, N = 200, 1001  # 200 Hz sampling rate for almost 5 s signal
    t_z = np.arange(N) / fs  # time indexes for signal
    z = np.exp(2j*np.pi*70 * (t_z - 0.2*t_z**2))  # complex-valued sweep

    nperseg, noverlap = 50, 40
    win = ('gaussian', 1e-2 * fs)  # Gaussian with 0.01 s standard dev.

    # Legacy spectrogram:
    f2_u, t2, Sz2_u = spectrogram(z, fs, win, nperseg, noverlap, detrend=None,
                                  return_onesided=False, scaling='spectrum',
                                  mode='complex')

    f2, Sz2 = fftshift(f2_u), fftshift(Sz2_u, axes=0)

    # New STFT:
    SFT = ShortTimeFFT.from_window(win, fs, nperseg, noverlap,
                                   fft_mode='centered', scale_to='magnitude',
                                   phase_shift=None)
    Sz3 = SFT.stft(z, p0=0, p1=(N-noverlap) // SFT.hop, k_offset=nperseg // 2)
    t3 = SFT.t(N, p0=0, p1=(N-noverlap) // SFT.hop, k_offset=nperseg // 2)

    xp_assert_close(t2, t3)
    xp_assert_close(f2, SFT.f)
    xp_assert_close(Sz2, Sz3)

