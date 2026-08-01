
def test_hist_step_bottom_geometry():
    bins = [0, 1, 2, 3]
    data = [0, 0, 1, 1, 1, 2]
    top = [[0, 1], [0, 3], [1, 3], [1, 5], [2, 5], [2, 2.5], [3, 2.5], [3, 1.5]]
    bottom = [[2, 1.5], [2, 2], [1, 2], [1, 1], [0, 1]]

    for histtype, xy in [('step', top), ('stepfilled', top + bottom)]:
        _, _, (polygon, ) = plt.hist(data, bins=bins, bottom=[1, 2, 1.5],
                                     histtype=histtype)
        assert_array_equal(polygon.get_xy(), xy)

