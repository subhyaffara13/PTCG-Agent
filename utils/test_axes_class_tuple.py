
def test_axes_class_tuple():
    fig = plt.figure()
    axes_class = (mpl_toolkits.axes_grid1.mpl_axes.Axes, {})
    gr = AxesGrid(fig, 111, nrows_ncols=(1, 1), axes_class=axes_class)

