
def test_affine_fill_to_edges():
    # The two rows show the two settings of origin
    # The three columns show the original and the two mirror flips
    fig, axs = plt.subplots(2, 3)

    N = 7
    data = np.arange(N**2).reshape((N, N)) % 3

    transform = [Affine2D(),
                 Affine2D().translate(0, -N + 1).scale(1, -1),
                 Affine2D().translate(-N + 1, 0).scale(-1, 1)]

    for j in range(3):
        for i in range(2):
            origin = 'upper' if i == 0 else 'lower'

            axs[i, j].imshow(data, cmap='Grays',
                             interpolation='hanning', origin=origin,
                             transform=transform[j] + axs[i, j].transData)

            axs[i, j].set_axis_off()
            axs[i, j].vlines([-0.5, N - 0.5], -1, 2, lw=0.5, color='red')
            axs[i, j].vlines([-0.5, N - 0.5], N - 3, N, lw=0.5, color='red')
            axs[i, j].hlines([-0.5, N - 0.5], -1, 2, lw=0.5, color='red')
            axs[i, j].hlines([-0.5, N - 0.5], N - 3, N, lw=0.5, color='red')

