
def test_calculation():

    a = ImmutableDenseNDimArray([1]*9, (3, 3))
    b = ImmutableDenseNDimArray([9]*9, (3, 3))

    c = a + b
    for i in c:
        assert i == ImmutableDenseNDimArray([10, 10, 10])

    assert c == ImmutableDenseNDimArray([10]*9, (3, 3))
    assert c == ImmutableSparseNDimArray([10]*9, (3, 3))

    c = b - a
    for i in c:
        assert i == ImmutableDenseNDimArray([8, 8, 8])

    assert c == ImmutableDenseNDimArray([8]*9, (3, 3))
    assert c == ImmutableSparseNDimArray([8]*9, (3, 3))


def test_calculation():

    a = MutableDenseNDimArray([1]*9, (3, 3))
    b = MutableDenseNDimArray([9]*9, (3, 3))

    c = a + b
    for i in c:
        assert i == MutableDenseNDimArray([10, 10, 10])

    assert c == MutableDenseNDimArray([10]*9, (3, 3))
    assert c == MutableSparseNDimArray([10]*9, (3, 3))

    c = b - a
    for i in c:
        assert i == MutableSparseNDimArray([8, 8, 8])

    assert c == MutableDenseNDimArray([8]*9, (3, 3))
    assert c == MutableSparseNDimArray([8]*9, (3, 3))

