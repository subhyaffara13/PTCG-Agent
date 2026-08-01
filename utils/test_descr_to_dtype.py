
def test_descr_to_dtype(dt):
    dt1 = format.descr_to_dtype(dt.descr)
    assert_equal_(dt1, dt)
    arr1 = np.zeros(3, dt)
    arr2 = roundtrip(arr1)
    assert_array_equal(arr1, arr2)

