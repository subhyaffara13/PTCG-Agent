
def test_dtype_closed_mismatch():
    # GH#38394 closed specified in both dtype and IntervalIndex constructor

    dtype = IntervalDtype(np.int64, "left")

    msg = "closed keyword does not match dtype.closed"
    with pytest.raises(ValueError, match=msg):
        IntervalIndex([], dtype=dtype, closed="neither")

    with pytest.raises(ValueError, match=msg):
        IntervalArray([], dtype=dtype, closed="neither")

