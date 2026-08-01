
def test_nonuniform_logscale():
    _, axs = plt.subplots(ncols=3, nrows=1)

    for i in range(3):
        ax = axs[i]
        im = NonUniformImage(ax)
        im.set_data(np.arange(1, 4) ** 2, np.arange(1, 4) ** 2,
                    np.arange(9).reshape((3, 3)))
        ax.set_xlim(1, 16)
        ax.set_ylim(1, 16)
        ax.set_box_aspect(1)
        if i == 1:
            ax.set_xscale("log", base=2)
            ax.set_yscale("log", base=2)
        if i == 2:
            ax.set_xscale("log", base=4)
            ax.set_yscale("log", base=4)
        ax.add_image(im)

