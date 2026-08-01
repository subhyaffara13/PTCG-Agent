
def test_writeable():
    # broadcast_to should return a readonly array
    original = np.array([1, 2, 3])
    result = broadcast_to(original, (2, 3))
    assert_equal(result.flags.writeable, False)
    assert_raises(ValueError, result.__setitem__, slice(None), 0)

    # but the result of broadcast_arrays needs to be writeable, to
    # preserve backwards compatibility
    test_cases = [((False,), broadcast_arrays(original,)),
                  ((True, False), broadcast_arrays(0, original))]
    for is_broadcast, results in test_cases:
        for array_is_broadcast, result in zip(is_broadcast, results):
            # This will change to False in a future version
            if array_is_broadcast:
                with pytest.warns(FutureWarning):
                    assert_equal(result.flags.writeable, True)
                with pytest.warns(DeprecationWarning):
                    result[:] = 0
                # Warning not emitted, writing to the array resets it
                assert_equal(result.flags.writeable, True)
            else:
                # No warning:
                assert_equal(result.flags.writeable, True)

    for results in [broadcast_arrays(original),
                    broadcast_arrays(0, original)]:
        for result in results:
            # resets the warn_on_write DeprecationWarning
            result.flags.writeable = True
            # check: no warning emitted
            assert_equal(result.flags.writeable, True)
            result[:] = 0

    # keep readonly input readonly
    original.flags.writeable = False
    _, result = broadcast_arrays(0, original)
    assert_equal(result.flags.writeable, False)

    # regression test for GH6491
    shape = (2,)
    strides = [0]
    tricky_array = as_strided(np.array(0), shape, strides)
    other = np.zeros((1,))
    first, second = broadcast_arrays(tricky_array, other)
    assert_(first.shape == second.shape)

