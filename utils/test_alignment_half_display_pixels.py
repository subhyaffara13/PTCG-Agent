
def test_alignment_half_display_pixels(nonaffine_identity):
    # All values in this test are chosen carefully so that many display pixels are
    # aligned with an edge or a corner of an input pixel

    # Layout:
    # Top row is origin='upper', bottom row is origin='lower'
    # Column 1: affine transform, anchored at whole pixel
    # Column 2: affine transform, anchored at half pixel
    # Column 3: nonaffine transform, anchored at whole pixel
    # Column 4: nonaffine transform, anchored at half pixel
    # Column 5: affine transform, anchored at half pixel, interpolation='hanning'

    # Each axes patch is magenta, so seeing a magenta line at an edge of the image
    # means that the image is not filling the axes

    fig = plt.figure(figsize=(5, 2), dpi=100)
    fig.set_facecolor('g')

    corner_x = [0.01, 0.199, 0.41, 0.599, 0.809]
    corner_y = [0.05, 0.53]

    axs = []
    for cy in corner_y:
        for ix, cx in enumerate(corner_x):
            my = cy + 0.0125 if ix in [1, 3, 4] else cy
            axs.append(fig.add_axes([cx, my, 0.17, 0.425], xticks=[], yticks=[]))

    # Verify that each axes has been created with the correct width/height and that all
    # four corners are on whole pixels (columns 1 and 3) or half pixels (columns 2, 4,
    # and 5)
    for i, ax in enumerate(axs):
        extents = ax.get_window_extent().extents
        assert_allclose(extents[2:4] - extents[0:2], 85, rtol=0, atol=1e-13)
        assert_allclose(extents % 1, 0.5 if i % 5 in [1, 3, 4] else 0,
                        rtol=0, atol=1e-13)

    N = 10

    data = np.arange(N**2).reshape((N, N)) % 9
    seps = np.arange(-0.5, N)

    for i, ax in enumerate(axs):
        ax.set_facecolor('m')

        transform = nonaffine_identity + ax.transData if i % 4 >= 2 else ax.transData
        ax.imshow(data, cmap='Blues',
                  interpolation='hanning' if i % 5 == 4 else 'nearest',
                  origin='upper' if i >= 5 else 'lower',
                  transform=transform)

        ax.vlines(seps, -0.5, N - 0.5, lw=0.5, color='red', ls=(0, (2, 4)))
        ax.hlines(seps, -0.5, N - 0.5, lw=0.5, color='red', ls=(0, (2, 4)))

        for spine in ax.spines:
            ax.spines[spine].set_linestyle((0, (5, 10)))

