
def test_contour_set_paths(fig_test, fig_ref):
    cs_test = fig_test.subplots().contour([[0, 1], [1, 2]])
    cs_ref = fig_ref.subplots().contour([[1, 0], [2, 1]])

    cs_test.set_paths(cs_ref.get_paths())

