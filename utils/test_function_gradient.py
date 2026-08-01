
def test_function_gradient(styler, f):
    for c_map in [None, "YlOrRd"]:
        result = getattr(styler, f)(cmap=c_map)._compute().ctx
        assert all("#" in x[0][1] for x in result.values())
        assert result[(0, 0)] == result[(0, 1)]
        assert result[(1, 0)] == result[(1, 1)]

