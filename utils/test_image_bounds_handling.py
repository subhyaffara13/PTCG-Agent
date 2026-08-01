
def test_image_bounds_handling(nonaffine_identity):
    # TODO: The second and third panels in the bottom row show that the handling of
    # image bounds is bugged for non-affine transforms and non-nearest-neighbor
    # interpolation.  If this bug gets fixed, the baseline image should be updated.

    fig, axs = plt.subplots(2, 3)

    N = 11

    for j, interpolation in enumerate(['nearest', 'hanning', 'bilinear']):
        data = np.arange(N**2).reshape((N, N))
        data = data / N**2 + (data % 4) / 6
        rotation = Affine2D().rotate_around(N/2-0.5, N/2-0.5, 1)

        for i in range(2):
            transform = rotation + axs[i, j].transData
            if i == 1:
                # Bottom row uses a non-affine transform
                transform = nonaffine_identity + transform

            axs[i, j].imshow(data, cmap='Grays', interpolation=interpolation,
                             transform=transform)

            axs[i, j].set_axis_off()
            box = Rectangle((-0.5, -0.5), N, N,
                            edgecolor='red', facecolor='none', lw=0.5, ls='dashed',
                            transform=rotation + axs[i, j].transData)
            axs[i, j].add_artist(box)

