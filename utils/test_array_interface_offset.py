
def test_array_interface_offset():
    arr = np.array([1, 2, 3], dtype='int32')
    interface = dict(arr.__array_interface__)
    interface['data'] = memoryview(arr)
    interface['shape'] = (2,)
    interface['offset'] = 4

    class DummyArray:
        __array_interface__ = interface

    arr1 = np.asarray(DummyArray())
    assert_equal(arr1, arr[1:])

