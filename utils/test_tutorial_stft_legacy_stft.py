
def test_tutorial_stft_legacy_stft():
    """Verify STFT example in "Comparison with Legacy Implementation" from the
    "User Guide".

    In :ref:`tutorial_stft_legacy_stft` (file ``signal.rst``) of the
    :ref:`user_guide` the legacy and the new implementation are compared.
    """
    fs, N = 200, 1001  # # 200 Hz sampling rate for 5 s signal
    t_z = np.arange(N) / fs  # time indexes for signal
    z = np.exp(2j*np.pi * 70 * (t_z - 0.2 * t_z ** 2))  # complex-valued chirp

    nperseg, noverlap = 50, 40
    win = ('gaussian', 1e-2 * fs)  # Gaussian with 0.01 s standard deviation

    # Legacy STFT:
    f0_u, t0, Sz0_u = stft(z, fs, win, nperseg, noverlap,
                           return_onesided=False, scaling='spectrum')
    Sz0 = fftshift(Sz0_u, axes=0)

    # New STFT:
    SFT = ShortTimeFFT.from_window(win, fs, nperseg, noverlap,
                                   fft_mode='centered',
                                   scale_to='magnitude', phase_shift=None)
    Sz1 = SFT.stft(z)

    xp_assert_close(Sz0, Sz1[:, 2:-1])

    xp_assert_close((abs(Sz1[:, 1]).min(), abs(Sz1[:, 1]).max()),
                    (6.925060911593139e-07, 8.00271269218721e-07))

    t0_r, z0_r = istft(Sz0_u, fs, win, nperseg, noverlap, input_onesided=False,
                       scaling='spectrum')
    z1_r = SFT.istft(Sz1, k1=N)
    assert len(z0_r) == N + 9
    xp_assert_close(z0_r[:N], z)
    xp_assert_close(z1_r, z)

    #  Spectrogram is just the absolute square of th STFT:
    xp_assert_close(SFT.spectrogram(z), abs(Sz1) ** 2)

