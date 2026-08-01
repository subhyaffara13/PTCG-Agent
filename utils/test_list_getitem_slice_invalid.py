
def test_list_getitem_slice_invalid():
    ser = Series(
        [[1, 2, 3], [4, None, 5], None],
        dtype=ArrowDtype(pa.list_(pa.int64())),
    )
    with tm.external_error_raised(pa.ArrowInvalid):
        ser.list[1:None:0]

