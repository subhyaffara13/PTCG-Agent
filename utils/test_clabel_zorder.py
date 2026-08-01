
def test_clabel_zorder(use_clabeltext, contour_zorder, clabel_zorder):
    x, y = np.meshgrid(np.arange(0, 10), np.arange(0, 10))
    z = np.max(np.dstack([abs(x), abs(y)]), 2)

    fig, ax = plt.subplots()
    cs = ax.contour(x, y, z, zorder=contour_zorder)
    clabels = cs.clabel(zorder=clabel_zorder, use_clabeltext=use_clabeltext)

    if clabel_zorder is None:
        expected_clabel_zorder = 2+contour_zorder
    else:
        expected_clabel_zorder = clabel_zorder

    for clabel in clabels:
        assert clabel.get_zorder() == expected_clabel_zorder

