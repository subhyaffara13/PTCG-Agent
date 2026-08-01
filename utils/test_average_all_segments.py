
def test_average_all_segments():
    """Compare `welch` function with stft mean.

    Ported from `TestSpectrogram.test_average_all_segments` from file
    ``test__spectral.py``.
    """
    x = np.random.randn(1024)

    fs = 1.0
    window = ('tukey', 0.25)
    nperseg, noverlap = 16, 2
    fw, Pw = welch(x, fs, window, nperseg, noverlap)
    SFT = ShortTimeFFT.from_window(window, fs, nperseg, noverlap,
                                   fft_mode='onesided2X', scale_to='psd',
                                   phase_shift=None)
    # `welch` positions the window differently than the STFT:
    P = SFT.spectrogram(x, detr='constant', p0=0,
                        p1=(len(x)-noverlap)//SFT.hop, k_offset=nperseg//2)

    xp_assert_close(SFT.f, fw)
    xp_assert_close(np.mean(P, axis=-1), Pw)

