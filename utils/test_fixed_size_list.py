
def test_fixed_size_list():
    # GH#55000
    ser = pd.Series(
        [[1, 2], [3, 4]], dtype=ArrowDtype(pa.list_(pa.int64(), list_size=2))
    )
    result = ser.dtype.type
    assert result == list

