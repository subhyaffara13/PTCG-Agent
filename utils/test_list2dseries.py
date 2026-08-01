
def test_list2dseries():
    if not np:
        skip("numpy not installed.")

    xx = np.linspace(-3, 3, 10)
    yy1 = np.cos(xx)
    yy2 = np.linspace(-3, 3, 20)

    # same number of elements: everything is fine
    s = List2DSeries(xx, yy1)
    assert not s.is_parametric
    # different number of elements: error
    raises(ValueError, lambda: List2DSeries(xx, yy2))

    # no color func: returns only x, y components and s in not parametric
    s = List2DSeries(xx, yy1)
    xxs, yys = s.get_data()
    assert np.allclose(xx, xxs)
    assert np.allclose(yy1, yys)
    assert not s.is_parametric

