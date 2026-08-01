
def test_nonuniform_and_pcolor():
    axs = plt.figure(figsize=(3, 3)).subplots(3, sharex=True, sharey=True)
    for ax, interpolation in zip(axs, ["nearest", "bilinear"]):
        im = NonUniformImage(ax, interpolation=interpolation)
        im.set_data(np.arange(3) ** 2, np.arange(3) ** 2,
                    np.arange(9).reshape((3, 3)))
        ax.add_image(im)
    axs[2].pcolorfast(  # PcolorImage
        np.arange(4) ** 2, np.arange(4) ** 2, np.arange(9).reshape((3, 3)))
    for ax in axs:
        ax.set_axis_off()
        # NonUniformImage "leaks" out of extents, not PColorImage.
        ax.set(xlim=(0, 10))

