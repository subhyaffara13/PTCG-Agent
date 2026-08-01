
def test_set_dict_to_rgba():
    # downstream libraries do this...
    # note we can't test this because it is not well-ordered
    # so just smoketest:
    colors = {(0, .5, 1), (1, .2, .5), (.4, 1, .2)}
    res = mcolors.to_rgba_array(colors)
    palette = {"red": (1, 0, 0), "green": (0, 1, 0), "blue": (0, 0, 1)}
    res = mcolors.to_rgba_array(palette.values())
    exp = np.eye(3)
    np.testing.assert_array_almost_equal(res[:, :-1], exp)

