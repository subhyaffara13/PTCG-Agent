
def test_rational_dtype(rat_cls):
    # test for bug gh-5719
    a = np.array([1111], dtype=rat_cls).astype
    assert_raises(OverflowError, a, 'int8')

    # test that dtype detection finds user-defined types
    x = rat_cls(1)
    assert np.array([x, x]).dtype.type is rat_cls

