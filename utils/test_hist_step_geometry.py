
def test_hist_step_geometry():
    bins = [0, 1, 2, 3]
    data = [0, 0, 1, 1, 1, 2]
    top = [[0, 0], [0, 2], [1, 2], [1, 3], [2, 3], [2, 1], [3, 1], [3, 0]]
    bottom = [[2, 0], [2, 0], [1, 0], [1, 0], [0, 0]]

    for histtype, xy in [('step', top), ('stepfilled', top + bottom)]:
        _, _, (polygon, ) = plt.hist(data, bins=bins, histtype=histtype)
        assert_array_equal(polygon.get_xy(), xy)

