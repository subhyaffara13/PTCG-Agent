
def test_rgba_antialias():
    fig, axs = plt.subplots(2, 2, figsize=(3.5, 3.5), sharex=False,
                            sharey=False, constrained_layout=True)
    N = 250
    aa = np.ones((N, N))
    aa[::2, :] = -1

    x = np.arange(N) / N - 0.5
    y = np.arange(N) / N - 0.5

    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    f0 = 10
    k = 75
    # aliased concentric circles
    a = np.sin(np.pi * 2 * (f0 * R + k * R**2 / 2))

    # stripes on lhs
    a[:int(N/2), :][R[:int(N/2), :] < 0.4] = -1
    a[:int(N/2), :][R[:int(N/2), :] < 0.3] = 1
    aa[:, int(N/2):] = a[:, int(N/2):]

    # set some over/unders and NaNs
    aa[20:50, 20:50] = np.nan
    aa[70:90, 70:90] = 1e6
    aa[70:90, 20:30] = -1e6
    aa[70:90, 195:215] = 1e6
    aa[20:30, 195:215] = -1e6

    cmap = plt.colormaps["RdBu_r"].with_extremes(over='yellow', under='cyan')

    axs = axs.flatten()
    # zoom in
    axs[0].imshow(aa, interpolation='nearest', cmap=cmap, vmin=-1.2, vmax=1.2)
    axs[0].set_xlim(N/2-25, N/2+25)
    axs[0].set_ylim(N/2+50, N/2-10)

    # no anti-alias
    axs[1].imshow(aa, interpolation='nearest', cmap=cmap, vmin=-1.2, vmax=1.2)

    # data antialias: Note no purples, and white in circle.  Note
    # that alternating red and blue stripes become white.
    axs[2].imshow(aa, interpolation='auto', interpolation_stage='data',
                  cmap=cmap, vmin=-1.2, vmax=1.2)

    # rgba antialias: Note purples at boundary with circle.  Note that
    # alternating red and blue stripes become purple
    axs[3].imshow(aa, interpolation='auto', interpolation_stage='rgba',
                  cmap=cmap, vmin=-1.2, vmax=1.2)

