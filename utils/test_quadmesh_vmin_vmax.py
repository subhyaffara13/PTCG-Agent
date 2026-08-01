
def test_quadmesh_vmin_vmax(pcfunc):
    # test when vmin/vmax on the norm changes, the quadmesh gets updated
    fig, ax = plt.subplots()
    cmap = mpl.colormaps['plasma']
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    coll = getattr(ax, pcfunc)([[1]], cmap=cmap, norm=norm)
    fig.canvas.draw()
    assert np.array_equal(coll.get_facecolors()[0, :], cmap(norm(1)))

    # Change the vmin/vmax of the norm so that the color is from
    # the bottom of the colormap now
    norm.vmin, norm.vmax = 1, 2
    fig.canvas.draw()
    assert np.array_equal(coll.get_facecolors()[0, :], cmap(norm(1)))

