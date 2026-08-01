
def test_axisline_style_tight():
    # Remove this line when this test image is regenerated.
    plt.rcParams.update({"xtick.direction": "in", "ytick.direction": "in"})
    fig = plt.figure(figsize=(2, 2), layout='tight')
    ax = fig.add_subplot(axes_class=AxesZero)
    ax.axis["xzero"].set_axisline_style("-|>", size=5, facecolor='g')
    ax.axis["xzero"].set_visible(True)
    ax.axis["yzero"].set_axisline_style("->, size=8")
    ax.axis["yzero"].set_visible(True)

    for direction in ("left", "right", "bottom", "top"):
        ax.axis[direction].set_visible(False)

