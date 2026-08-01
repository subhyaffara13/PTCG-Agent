
def test_psd_csd():
    n = 10000
    Fs = 100.

    fstims = [[Fs/4, Fs/5, Fs/11], [Fs/4.7, Fs/5.6, Fs/11.9]]
    NFFT_freqs = int(1000 * Fs / np.min(fstims))
    x = np.arange(0, n, 1/Fs)
    ys_freqs = np.sin(2 * np.pi * np.multiply.outer(fstims, x)).sum(axis=1)

    NFFT_noise = int(1000 * Fs / 11)
    np.random.seed(0)
    ys_noise = [np.random.standard_normal(n), np.random.rand(n)]

    all_kwargs = [{"sides": "default"},
                  {"sides": "onesided", "return_line": False},
                  {"sides": "twosided", "return_line": True}]
    for ys, NFFT in [(ys_freqs, NFFT_freqs), (ys_noise, NFFT_noise)]:
        noverlap = NFFT // 2
        pad_to = int(2 ** np.ceil(np.log2(NFFT)))
        for ax, kwargs in zip(plt.figure().subplots(3), all_kwargs):
            ret = ax.psd(np.concatenate(ys), NFFT=NFFT, Fs=Fs,
                         noverlap=noverlap, pad_to=pad_to, **kwargs)
            assert len(ret) == 2 + kwargs.get("return_line", False)
            ax.set(xlabel="", ylabel="")
        for ax, kwargs in zip(plt.figure().subplots(3), all_kwargs):
            ret = ax.csd(*ys, NFFT=NFFT, Fs=Fs,
                         noverlap=noverlap, pad_to=pad_to, **kwargs)
            assert len(ret) == 2 + kwargs.get("return_line", False)
            ax.set(xlabel="", ylabel="")

