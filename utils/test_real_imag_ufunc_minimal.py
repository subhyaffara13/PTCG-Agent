
def test_real_imag_ufunc_minimal(ufunc, attr):
    with pytest.raises(TypeError):
        ufunc(np.array([1, 2, 3]))  # non-complex or object raises

    arr = np.array([1 + 2j, 3 + 4j])
    res = ufunc(arr)
    assert_array_equal(res, getattr(arr, attr), strict=True)

    arr = np.array([1 + 2j, 3 + 4j], dtype=object)
    res = ufunc(arr)
    assert_array_equal(res, getattr(arr, attr), strict=True)

