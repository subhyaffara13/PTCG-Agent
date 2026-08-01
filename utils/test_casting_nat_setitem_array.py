
def test_casting_nat_setitem_array(arr, casting_nats):
    expected = type(arr)._from_sequence([NaT, arr[1], arr[2]], dtype=arr.dtype)

    for nat in casting_nats:
        arr = arr.copy()
        arr[0] = nat
        tm.assert_equal(arr, expected)

