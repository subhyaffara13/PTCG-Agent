
def test_writeable_memoryview():
    # The result of broadcast_arrays exports as a non-writeable memoryview
    # because otherwise there is no good way to opt in to the new behaviour
    # (i.e. you would need to set writeable to False explicitly).
    # See gh-13929.
    original = np.array([1, 2, 3])

    test_cases = [((False, ), broadcast_arrays(original,)),
                  ((True, False), broadcast_arrays(0, original))]
    for is_broadcast, results in test_cases:
        for array_is_broadcast, result in zip(is_broadcast, results):
            # This will change to False in a future version
            if array_is_broadcast:
                # memoryview(result, writable=True) will give warning but cannot
                # be tested using the python API.
                assert memoryview(result).readonly
            else:
                assert not memoryview(result).readonly

