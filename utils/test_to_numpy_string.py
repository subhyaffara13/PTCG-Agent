
def test_to_numpy_string(box, dtype):
    con = pd.Series if box else pd.array
    arr = con([0.0, 1.0, None], dtype="Float64")

    result = arr.to_numpy(dtype="str")
    expected = np.array([0.0, 1.0, pd.NA], dtype=f"{tm.ENDIAN}U32")
    tm.assert_numpy_array_equal(result, expected)

