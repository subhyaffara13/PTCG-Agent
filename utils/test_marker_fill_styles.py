import itertools

def test_marker_fill_styles():
    colors = itertools.cycle([[0, 0, 1], 'g', '#ff0000', 'c', 'm', 'y',
                              np.array([0, 0, 0])])
    altcolor = 'lightgreen'

    y = np.array([1, 1])
    x = np.array([0, 9])
    fig, ax = plt.subplots()

    # This hard-coded list of markers correspond to an earlier iteration of
    # MarkerStyle.filled_markers; the value of that attribute has changed but
    # we kept the old value here to not regenerate the baseline image.
    # Replace with mlines.Line2D.filled_markers when the image is regenerated.
    for j, marker in enumerate("ov^<>8sp*hHDdPX"):
        for i, fs in enumerate(mlines.Line2D.fillStyles):
            color = next(colors)
            ax.plot(j * 10 + x, y + i + .5 * (j % 2),
                    marker=marker,
                    markersize=20,
                    markerfacecoloralt=altcolor,
                    fillstyle=fs,
                    label=fs,
                    linewidth=5,
                    color=color,
                    markeredgecolor=color,
                    markeredgewidth=2)

    ax.set_ylim(0, 7.5)
    ax.set_xlim(-5, 155)

