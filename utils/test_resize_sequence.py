
def test_resize_sequence():
    a_list = [1, 2, 3]
    arr = np.array([1, 2, 3])

    # already same length: passthrough
    assert cbook._resize_sequence(a_list, 3) is a_list
    assert cbook._resize_sequence(arr, 3) is arr

    # shortening
    assert cbook._resize_sequence(a_list, 2) == [1, 2]
    assert_array_equal(cbook._resize_sequence(arr, 2), [1, 2])

    # extending
    assert cbook._resize_sequence(a_list, 5) == [1, 2, 3, 1, 2]
    assert_array_equal(cbook._resize_sequence(arr, 5), [1, 2, 3, 1, 2])

