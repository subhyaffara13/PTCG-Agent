
def as_strided_writeable():
    arr = np.ones(10)
    view = as_strided(arr, writeable=False)
    assert_(not view.flags.writeable)

    # Check that writeable also is fine:
    view = as_strided(arr, writeable=True)
    assert_(view.flags.writeable)
    view[...] = 3
    assert_array_equal(arr, np.full_like(arr, 3))

    # Test that things do not break down for readonly:
    arr.flags.writeable = False
    view = as_strided(arr, writeable=False)
    view = as_strided(arr, writeable=True)
    assert_(not view.flags.writeable)

