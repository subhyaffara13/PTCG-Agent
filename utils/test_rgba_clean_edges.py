
def test_rgba_clean_edges():
    np.random.seed(19680801+9)  # same as in test_upsampling()
    data = np.random.rand(8, 8)
    data = np.stack([data, data])
    data[1, 2:4, 2:4] = np.nan

    rotation = Affine2D().rotate_around(3.5, 3.5, 1)

    fig, axs = plt.subplots(1, 2)

    for i in range(2):
        # Add background patches to check the fading to non-white colors
        black = Rectangle((3.75, 2), 5, 5, color='black', zorder=0)
        gray = Rectangle((0, -2), 3.75, 4, color='gray', zorder=0)
        partly_black = Rectangle((3.75, -2), 5, 4, fc='black', ec='none',
                                 alpha=0.5, zorder=0)
        axs[i].add_patch(black)
        axs[i].add_patch(gray)
        axs[i].add_patch(partly_black)

        axs[i].imshow(data[i, ...],
                      interpolation='bilinear', interpolation_stage='rgba',
                      transform=rotation + axs[i].transData)

        axs[i].set_axis_off()
        axs[i].set_xlim(-2.5, 9.5)
        axs[i].set_ylim(-2.5, 9.5)

