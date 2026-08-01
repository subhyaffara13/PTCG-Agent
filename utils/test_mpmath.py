
def test_mpmath():
    # test that the argument of complex functions evaluated with mpmath
    # might be different than the one computed with Numpy (different
    # behaviour at branch cuts)
    if not np:
        skip("numpy not installed.")

    z, u = symbols("z, u")

    s1 = LineOver1DRangeSeries(im(sqrt(-z)), (z, 1e-03, 5),
        adaptive=True, modules=None, force_real_eval=True)
    s2 = LineOver1DRangeSeries(im(sqrt(-z)), (z, 1e-03, 5),
        adaptive=True, modules="mpmath", force_real_eval=True)
    xx1, yy1 = s1.get_data()
    xx2, yy2 = s2.get_data()
    assert np.all(yy1 < 0)
    assert np.all(yy2 > 0)

    s1 = LineOver1DRangeSeries(im(sqrt(-z)), (z, -5, 5),
        adaptive=False, n=20, modules=None, force_real_eval=True)
    s2 = LineOver1DRangeSeries(im(sqrt(-z)), (z, -5, 5),
        adaptive=False, n=20, modules="mpmath", force_real_eval=True)
    xx1, yy1 = s1.get_data()
    xx2, yy2 = s2.get_data()
    assert np.allclose(xx1, xx2)
    assert not np.allclose(yy1, yy2)

