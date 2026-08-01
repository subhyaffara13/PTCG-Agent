
def test_grid_with_axes_class_not_overriding_axis():
    Grid(plt.figure(), 111, (2, 2), axes_class=mpl.axes.Axes)
    RGBAxes(plt.figure(), 111, axes_class=mpl.axes.Axes)

