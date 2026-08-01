
def test_array_interface_empty_shape():
    # See gh-7994
    arr = np.array([1, 2, 3])
    interface1 = dict(arr.__array_interface__)
    interface1['shape'] = ()

    class DummyArray1:
        __array_interface__ = interface1

    # NOTE: Because Py2 str/Py3 bytes supports the buffer interface, setting
    # the interface data to bytes would invoke the bug this tests for, that
    # __array_interface__ with shape=() is not allowed if the data is an object
    # exposing the buffer interface
    interface2 = dict(interface1)
    interface2['data'] = arr[0].tobytes()

    class DummyArray2:
        __array_interface__ = interface2

    arr1 = np.asarray(DummyArray1())
    arr2 = np.asarray(DummyArray2())
    arr3 = arr[:1].reshape(())
    assert_equal(arr1, arr2)
    assert_equal(arr1, arr3)

