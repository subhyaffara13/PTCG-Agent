
def test_rasterize_dpi():
    # This test should check rasterized rendering with high output resolution.
    # It plots a rasterized line and a normal image with imshow.  So it will
    # catch when images end up in the wrong place in case of non-standard dpi
    # setting.  Instead of high-res rasterization I use low-res.  Therefore
    # the fact that the resolution is non-standard is easily checked by
    # image_comparison.
    img = np.asarray([[1, 2], [3, 4]])

    fig, axs = plt.subplots(1, 3, figsize=(3, 1))

    axs[0].imshow(img)

    axs[1].plot([0, 1], [0, 1], linewidth=20., rasterized=True)
    axs[1].set(xlim=(0, 1), ylim=(-1, 2))

    axs[2].plot([0, 1], [0, 1], linewidth=20.)
    axs[2].set(xlim=(0, 1), ylim=(-1, 2))

    # Low-dpi PDF rasterization errors prevent proper image comparison tests.
    # Hide detailed structures like the axes spines.
    for ax in axs:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines[:].set_visible(False)

    rcParams['savefig.dpi'] = 10

