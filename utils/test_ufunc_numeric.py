
def test_ufunc_numeric():
    # np.sqrt on np.bool_ returns float16, which we upcast to Float32
    #  bc we do not have Float16
    arr = pd.array([True, False, None], dtype="boolean")

    res = np.sqrt(arr)

    expected = pd.array([1, 0, None], dtype="Float32")
    tm.assert_extension_array_equal(res, expected)

