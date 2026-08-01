
def test_list2dseries_interactive():
    if not np:
        skip("numpy not installed.")

    x, y, u = symbols("x, y, u")

    s = List2DSeries([1, 2, 3], [1, 2, 3])
    assert not s.is_interactive

    # symbolic expressions as coordinates, but no ``params``
    raises(ValueError, lambda: List2DSeries([cos(x)], [sin(x)]))

    # too few parameters
    raises(ValueError,
        lambda: List2DSeries([cos(x), y], [sin(x), 2], params={u: 1}))

    s = List2DSeries([cos(x)], [sin(x)], params={x: 1})
    assert s.is_interactive

    s = List2DSeries([x, 2, 3, 4], [4, 3, 2, x], params={x: 3})
    xx, yy = s.get_data()
    assert np.allclose(xx, [3, 2, 3, 4])
    assert np.allclose(yy, [4, 3, 2, 3])
    assert not s.is_parametric

    # numeric lists + params is present -> interactive series and
    # lists are converted to Tuple.
    s = List2DSeries([1, 2, 3], [1, 2, 3], params={x: 1})
    assert s.is_interactive
    assert isinstance(s.list_x, Tuple)
    assert isinstance(s.list_y, Tuple)

