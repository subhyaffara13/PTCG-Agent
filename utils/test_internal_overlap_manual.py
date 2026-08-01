
def test_internal_overlap_manual():
    # Stride tricks can construct arrays with internal overlap

    # We don't care about memory bounds, the array is not
    # read/write accessed
    x = np.arange(1).astype(np.int8)

    # Check low-dimensional special cases

    check_internal_overlap(x, False)  # 1-dim
    check_internal_overlap(x.reshape([]), False)  # 0-dim

    a = as_strided(x, strides=(3, 4), shape=(4, 4))
    check_internal_overlap(a, False)

    a = as_strided(x, strides=(3, 4), shape=(5, 4))
    check_internal_overlap(a, True)

    a = as_strided(x, strides=(0,), shape=(0,))
    check_internal_overlap(a, False)

    a = as_strided(x, strides=(0,), shape=(1,))
    check_internal_overlap(a, False)

    a = as_strided(x, strides=(0,), shape=(2,))
    check_internal_overlap(a, True)

    a = as_strided(x, strides=(0, -9993), shape=(87, 22))
    check_internal_overlap(a, True)

    a = as_strided(x, strides=(0, -9993), shape=(1, 22))
    check_internal_overlap(a, False)

    a = as_strided(x, strides=(0, -9993), shape=(0, 22))
    check_internal_overlap(a, False)

