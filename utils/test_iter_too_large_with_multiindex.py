
def test_iter_too_large_with_multiindex():
    # When a multi index is being tracked, the error is delayed this
    # checks the delayed error messages and getting below that by
    # removing an axis.
    base_size = 2**10
    num = 1
    while base_size**num < np.iinfo(np.intp).max:
        num += 1

    shape_template = [1, 1] * num
    arrays = []
    for i in range(num):
        shape = shape_template[:]
        shape[i * 2] = 2**10
        arrays.append(np.empty(shape))
    arrays = tuple(arrays)

    # arrays are now too large to be broadcast. The different modes test
    # different nditer functionality with or without GIL.
    for mode in range(6):
        with assert_raises(ValueError):
            _multiarray_tests.test_nditer_too_large(arrays, -1, mode)
    # but if we do nothing with the nditer, it can be constructed:
    _multiarray_tests.test_nditer_too_large(arrays, -1, 7)

    # When an axis is removed, things should work again (half the time):
    for i in range(num):
        for mode in range(6):
            # an axis with size 1024 is removed:
            _multiarray_tests.test_nditer_too_large(arrays, i * 2, mode)
            # an axis with size 1 is removed:
            with assert_raises(ValueError):
                _multiarray_tests.test_nditer_too_large(arrays, i * 2 + 1, mode)

