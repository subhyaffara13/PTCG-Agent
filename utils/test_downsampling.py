
def test_downsampling():
    N = 450
    x = np.arange(N) / N - 0.5
    y = np.arange(N) / N - 0.5
    aa = np.ones((N, N))
    aa[::2, :] = -1

    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    f0 = 5
    k = 100
    a = np.sin(np.pi * 2 * (f0 * R + k * R**2 / 2))
    # make the left hand side of this
    a[:int(N / 2), :][R[:int(N / 2), :] < 0.4] = -1
    a[:int(N / 2), :][R[:int(N / 2), :] < 0.3] = 1
    aa[:, int(N / 3):] = a[:, int(N / 3):]
    a = aa

    fig, axs = plt.subplots(2, 3, figsize=(7, 6), layout='compressed')
    axs[0, 0].imshow(a, interpolation='nearest', interpolation_stage='rgba',
                     cmap='RdBu_r')
    axs[0, 0].set_xlim(125, 175)
    axs[0, 0].set_ylim(250, 200)
    axs[0, 0].set_title('Zoom')

    for ax, interp, space in zip(axs.flat[1:], ['nearest', 'nearest', 'hanning',
                                                'hanning', 'auto'],
                                 ['data', 'rgba', 'data', 'rgba', 'auto']):
        ax.imshow(a, interpolation=interp, interpolation_stage=space,
                  cmap='RdBu_r')
        ax.set_title(f"interpolation='{interp}'\nspace='{space}'")

