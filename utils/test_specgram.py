
def test_specgram():
    """Test axes.specgram in default (psd) mode."""

    # use former defaults to match existing baseline image
    matplotlib.rcParams['image.interpolation'] = 'nearest'

    n = 1000
    Fs = 10.

    fstims = [[Fs/4, Fs/5, Fs/11], [Fs/4.7, Fs/5.6, Fs/11.9]]
    NFFT_freqs = int(10 * Fs / np.min(fstims))
    x = np.arange(0, n, 1/Fs)
    y_freqs = np.concatenate(
        np.sin(2 * np.pi * np.multiply.outer(fstims, x)).sum(axis=1))

    NFFT_noise = int(10 * Fs / 11)
    np.random.seed(0)
    y_noise = np.concatenate([np.random.standard_normal(n), np.random.rand(n)])

    all_sides = ["default", "onesided", "twosided"]
    for y, NFFT in [(y_freqs, NFFT_freqs), (y_noise, NFFT_noise)]:
        noverlap = NFFT // 2
        pad_to = int(2 ** np.ceil(np.log2(NFFT)))
        for ax, sides in zip(plt.figure().subplots(3), all_sides):
            ax.specgram(y, NFFT=NFFT, Fs=Fs, noverlap=noverlap,
                        pad_to=pad_to, sides=sides)
        for ax, sides in zip(plt.figure().subplots(3), all_sides):
            ax.specgram(y, NFFT=NFFT, Fs=Fs, noverlap=noverlap,
                        pad_to=pad_to, sides=sides,
                        scale="linear", norm=matplotlib.colors.LogNorm())

