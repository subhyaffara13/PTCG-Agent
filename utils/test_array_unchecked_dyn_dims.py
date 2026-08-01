
def test_array_unchecked_dyn_dims():
    z1 = np.array([[1, 2], [3, 4]], dtype="float64")
    m.proxy_add2_dyn(z1, 10)
    assert np.all(z1 == [[11, 12], [13, 14]])

    expect_c = np.ndarray(shape=(3, 3, 3), buffer=np.array(range(3, 30)), dtype="int")
    assert np.all(m.proxy_init3_dyn(3.0) == expect_c)

    assert m.proxy_auxiliaries2_dyn(z1) == [11, 11, True, 2, 8, 2, 2, 4, 32]
    assert m.proxy_auxiliaries2_dyn(z1) == m.array_auxiliaries2(z1)

