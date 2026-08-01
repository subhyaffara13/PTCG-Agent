
def test_axisline_style_size_color():
    # Remove this line when this test image is regenerated.
    plt.rcParams.update({"xtick.direction": "in", "ytick.direction": "in"})
    fig = plt.figure(figsize=(2, 2))
    ax = fig.add_subplot(axes_class=AxesZero)
    ax.axis["xzero"].set_axisline_style("-|>", size=2.0, facecolor='r')
    ax.axis["xzero"].set_visible(True)
    ax.axis["yzero"].set_axisline_style("->, size=1.5")
    ax.axis["yzero"].set_visible(True)

    for direction in ("left", "right", "bottom", "top"):
        ax.axis[direction].set_visible(False)

