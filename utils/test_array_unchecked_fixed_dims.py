
def test_array_unchecked_fixed_dims(msg):
    z1 = np.array([[1, 2], [3, 4]], dtype="float64")
    m.proxy_add2(z1, 10)
    assert np.all(z1 == [[11, 12], [13, 14]])

    with pytest.raises(ValueError) as excinfo:
        m.proxy_add2(np.array([1.0, 2, 3]), 5.0)
    assert (
        msg(excinfo.value) == "array has incorrect number of dimensions: 1; expected 2"
    )

    expect_c = np.ndarray(shape=(3, 3, 3), buffer=np.array(range(3, 30)), dtype="int")
    assert np.all(m.proxy_init3(3.0) == expect_c)
    expect_f = np.transpose(expect_c)
    assert np.all(m.proxy_init3F(3.0) == expect_f)

    assert m.proxy_squared_L2_norm(np.array(range(6))) == 55
    assert m.proxy_squared_L2_norm(np.array(range(6), dtype="float64")) == 55

    assert m.proxy_auxiliaries2(z1) == [11, 11, True, 2, 8, 2, 2, 4, 32]
    assert m.proxy_auxiliaries2(z1) == m.array_auxiliaries2(z1)

    assert m.proxy_auxiliaries1_const_ref(z1[0, :])
    assert m.proxy_auxiliaries2_const_ref(z1)

