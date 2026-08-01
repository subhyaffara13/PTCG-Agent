
def test_nn_pixel_alignment(nonaffine_identity):
    fig, axs = plt.subplots(2, 3)

    for j, N in enumerate([3, 7, 11]):
        # In each column, the plots use the same data array
        data = np.arange(N**2).reshape((N, N)) % 4
        seps = np.arange(-0.5, N)

        for i in range(2):
            if i == 0:
                # Top row uses an affine transform
                axs[i, j].imshow(data, cmap='Grays', interpolation='nearest')
            else:
                # Bottom row uses a non-affine transform
                axs[i, j].imshow(data, cmap='Grays', interpolation='nearest',
                                 transform=nonaffine_identity + axs[i, j].transData)

            axs[i, j].set_axis_off()
            axs[i, j].vlines(seps, -1, N, lw=0.5, color='red', ls='dashed')
            axs[i, j].hlines(seps, -1, N, lw=0.5, color='red', ls='dashed')

