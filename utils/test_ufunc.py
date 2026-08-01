
def test_ufunc():
    assert_allclose(lambertw(r_[0., e, 1.]), r_[0., 1., 0.567143290409783873],
                    atol=1.5e-7, rtol=0)


def test_ufunc():
    assert np.log(NA) is NA
    assert np.add(NA, 1) is NA
    result = np.divmod(NA, 1)
    assert result[0] is NA and result[1] is NA

    result = np.frexp(NA)
    assert result[0] is NA and result[1] is NA


def test_ufunc():
    arr = NumpyExtensionArray(np.array([-1.0, 0.0, 1.0]))

    r1, r2 = np.divmod(arr, np.add(arr, 2))
    e1, e2 = np.divmod(arr._ndarray, np.add(arr._ndarray, 2))
    e1 = NumpyExtensionArray(e1)
    e2 = NumpyExtensionArray(e2)
    tm.assert_extension_array_equal(r1, e1)
    tm.assert_extension_array_equal(r2, e2)

