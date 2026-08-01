
def test_rcparam_grid_minor(grid_which, major_visible, minor_visible):
    mpl.rcParams.update({"axes.grid": True, "axes.grid.which": grid_which})
    fig, ax = plt.subplots()
    fig.canvas.draw()
    assert all(tick.gridline.get_visible() == major_visible
               for tick in ax.xaxis.majorTicks)
    assert all(tick.gridline.get_visible() == minor_visible
               for tick in ax.xaxis.minorTicks)

