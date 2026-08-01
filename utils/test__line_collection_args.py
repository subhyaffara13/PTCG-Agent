
def test_LineCollection_args():
    lc = LineCollection(None, linewidth=2.2, edgecolor='r',
                        zorder=3, facecolors=[0, 1, 0, 1])
    assert lc.get_linewidth()[0] == 2.2
    assert mcolors.same_color(lc.get_edgecolor(), 'r')
    assert lc.get_zorder() == 3
    assert mcolors.same_color(lc.get_facecolor(), [[0, 1, 0, 1]])
    # To avoid breaking mplot3d, LineCollection internally sets the facecolor
    # kwarg if it has not been specified.  Hence we need the following test
    # for LineCollection._set_default().
    lc = LineCollection(None, facecolor=None)
    assert mcolors.same_color(lc.get_facecolor(), 'none')

