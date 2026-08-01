
def test_astype_copies(dtype):
    # GH#50984
    pytest.importorskip("pyarrow")
    df = DataFrame({"a": [1, 2, 3]}, dtype=dtype)
    result = df.astype("int64[pyarrow]")
    df.iloc[0, 0] = 100
    expected = DataFrame({"a": [1, 2, 3]}, dtype="int64[pyarrow]")
    tm.assert_frame_equal(result, expected)


def test_astype_copies():
    arr = period_array(["2000", "2001", None], freq="D")
    result = arr.astype(np.int64, copy=False)

    # Add the `.base`, since we now use `.asi8` which returns a view.
    # We could maybe override it in PeriodArray to return ._ndarray directly.
    assert result.base is arr._ndarray

    result = arr.astype(np.int64, copy=True)
    assert result is not arr._ndarray
    tm.assert_numpy_array_equal(result, arr._ndarray.view("i8"))

