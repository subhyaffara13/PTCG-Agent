
def test_subplotzero_ylabel():
    fig = plt.figure()
    ax = fig.add_subplot(111, axes_class=SubplotZero)

    ax.set(xlim=(-3, 7), ylim=(-3, 7), xlabel="x", ylabel="y")

    zero_axis = ax.axis["xzero", "yzero"]
    zero_axis.set_visible(True)  # they are hidden by default

    ax.axis["left", "right", "bottom", "top"].set_visible(False)

    zero_axis.set_axisline_style("->")

