
def test_spectrum():
    n = 10000
    Fs = 100.

    fstims1 = [Fs/4, Fs/5, Fs/11]
    NFFT = int(1000 * Fs / min(fstims1))
    pad_to = int(2 ** np.ceil(np.log2(NFFT)))

    x = np.arange(0, n, 1/Fs)
    y_freqs = ((np.sin(2 * np.pi * np.outer(x, fstims1)) * 10**np.arange(3))
               .sum(axis=1))
    np.random.seed(0)
    y_noise = np.hstack([np.random.standard_normal(n), np.random.rand(n)]) - .5

    all_sides = ["default", "onesided", "twosided"]
    kwargs = {"Fs": Fs, "pad_to": pad_to}
    for y in [y_freqs, y_noise]:
        for ax, sides in zip(plt.figure().subplots(3), all_sides):
            spec, freqs, line = ax.magnitude_spectrum(y, sides=sides, **kwargs)
            ax.set(xlabel="", ylabel="")
        for ax, sides in zip(plt.figure().subplots(3), all_sides):
            spec, freqs, line = ax.magnitude_spectrum(y, sides=sides, **kwargs,
                                                      scale="dB")
            ax.set(xlabel="", ylabel="")
        for ax, sides in zip(plt.figure().subplots(3), all_sides):
            spec, freqs, line = ax.angle_spectrum(y, sides=sides, **kwargs)
            ax.set(xlabel="", ylabel="")
        for ax, sides in zip(plt.figure().subplots(3), all_sides):
            spec, freqs, line = ax.phase_spectrum(y, sides=sides, **kwargs)
            ax.set(xlabel="", ylabel="")

