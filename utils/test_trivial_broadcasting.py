
def test_trivial_broadcasting():
    trivial, vectorized_is_trivial = m.trivial, m.vectorized_is_trivial

    assert vectorized_is_trivial(1, 2, 3) == trivial.c_trivial
    assert vectorized_is_trivial(np.array(1), np.array(2), 3) == trivial.c_trivial
    assert (
        vectorized_is_trivial(np.array([1, 3]), np.array([2, 4]), 3)
        == trivial.c_trivial
    )
    assert trivial.c_trivial == vectorized_is_trivial(
        np.array([[1, 3, 5], [7, 9, 11]]), np.array([[2, 4, 6], [8, 10, 12]]), 3
    )
    assert (
        vectorized_is_trivial(np.array([[1, 2, 3], [4, 5, 6]]), np.array([2, 3, 4]), 2)
        == trivial.non_trivial
    )
    assert (
        vectorized_is_trivial(np.array([[1, 2, 3], [4, 5, 6]]), np.array([[2], [3]]), 2)
        == trivial.non_trivial
    )
    z1 = np.array([[1, 2, 3, 4], [5, 6, 7, 8]], dtype="int32")
    z2 = np.array(z1, dtype="float32")
    z3 = np.array(z1, dtype="float64")
    assert vectorized_is_trivial(z1, z2, z3) == trivial.c_trivial
    assert vectorized_is_trivial(1, z2, z3) == trivial.c_trivial
    assert vectorized_is_trivial(z1, 1, z3) == trivial.c_trivial
    assert vectorized_is_trivial(z1, z2, 1) == trivial.c_trivial
    assert vectorized_is_trivial(z1[::2, ::2], 1, 1) == trivial.non_trivial
    assert vectorized_is_trivial(1, 1, z1[::2, ::2]) == trivial.c_trivial
    assert vectorized_is_trivial(1, 1, z3[::2, ::2]) == trivial.non_trivial
    assert vectorized_is_trivial(z1, 1, z3[1::4, 1::4]) == trivial.c_trivial

    y1 = np.array(z1, order="F")
    y2 = np.array(y1)
    y3 = np.array(y1)
    assert vectorized_is_trivial(y1, y2, y3) == trivial.f_trivial
    assert vectorized_is_trivial(y1, 1, 1) == trivial.f_trivial
    assert vectorized_is_trivial(1, y2, 1) == trivial.f_trivial
    assert vectorized_is_trivial(1, 1, y3) == trivial.f_trivial
    assert vectorized_is_trivial(y1, z2, 1) == trivial.non_trivial
    assert vectorized_is_trivial(z1[1::4, 1::4], y2, 1) == trivial.f_trivial
    assert vectorized_is_trivial(y1[1::4, 1::4], z2, 1) == trivial.c_trivial

    assert m.vectorized_func(z1, z2, z3).flags.c_contiguous
    assert m.vectorized_func(y1, y2, y3).flags.f_contiguous
    assert m.vectorized_func(z1, 1, 1).flags.c_contiguous
    assert m.vectorized_func(1, y2, 1).flags.f_contiguous
    assert m.vectorized_func(z1[1::4, 1::4], y2, 1).flags.f_contiguous
    assert m.vectorized_func(y1[1::4, 1::4], z2, 1).flags.c_contiguous

