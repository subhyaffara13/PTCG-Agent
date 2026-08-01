
def test_reshape():
    seq = list(range(1, 9))
    assert reshape(seq, [4]) == \
        [[1, 2, 3, 4], [5, 6, 7, 8]]
    assert reshape(seq, (4,)) == \
        [(1, 2, 3, 4), (5, 6, 7, 8)]
    assert reshape(seq, (2, 2)) == \
        [(1, 2, 3, 4), (5, 6, 7, 8)]
    assert reshape(seq, (2, [2])) == \
        [(1, 2, [3, 4]), (5, 6, [7, 8])]
    assert reshape(seq, ((2,), [2])) == \
        [((1, 2), [3, 4]), ((5, 6), [7, 8])]
    assert reshape(seq, (1, [2], 1)) == \
        [(1, [2, 3], 4), (5, [6, 7], 8)]
    assert reshape(tuple(seq), ([[1], 1, (2,)],)) == \
        (([[1], 2, (3, 4)],), ([[5], 6, (7, 8)],))
    assert reshape(tuple(seq), ([1], 1, (2,))) == \
        (([1], 2, (3, 4)), ([5], 6, (7, 8)))
    assert reshape(list(range(12)), [2, [3], {2}, (1, (3,), 1)]) == \
        [[0, 1, [2, 3, 4], {5, 6}, (7, (8, 9, 10), 11)]]
    raises(ValueError, lambda: reshape([0, 1], [-1]))
    raises(ValueError, lambda: reshape([0, 1], [3]))


def test_reshape():
    array = ImmutableDenseNDimArray(range(50), 50)
    assert array.shape == (50,)
    assert array.rank() == 1

    array = array.reshape(5, 5, 2)
    assert array.shape == (5, 5, 2)
    assert array.rank() == 3
    assert len(array) == 50


def test_reshape():
    array = MutableDenseNDimArray(range(50), 50)
    assert array.shape == (50,)
    assert array.rank() == 1

    array = array.reshape(5, 5, 2)
    assert array.shape == (5, 5, 2)
    assert array.rank() == 3
    assert len(array) == 50


def test_reshape():
    m0 = eye_Shaping(3)
    assert m0.reshape(1, 9) == Matrix(1, 9, (1, 0, 0, 0, 1, 0, 0, 0, 1))
    m1 = ShapingOnlyMatrix(3, 4, lambda i, j: i + j)
    assert m1.reshape(
        4, 3) == Matrix(((0, 1, 2), (3, 1, 2), (3, 4, 2), (3, 4, 5)))
    assert m1.reshape(2, 6) == Matrix(((0, 1, 2, 3, 1, 2), (3, 4, 2, 3, 4, 5)))


def test_reshape():
    m0 = eye(3)
    assert m0.reshape(1, 9) == Matrix(1, 9, (1, 0, 0, 0, 1, 0, 0, 0, 1))
    m1 = Matrix(3, 4, lambda i, j: i + j)
    assert m1.reshape(
        4, 3) == Matrix(((0, 1, 2), (3, 1, 2), (3, 4, 2), (3, 4, 5)))
    assert m1.reshape(2, 6) == Matrix(((0, 1, 2, 3, 1, 2), (3, 4, 2, 3, 4, 5)))


def test_reshape():
    m0 = eye(3)
    assert m0.reshape(1, 9) == Matrix(1, 9, (1, 0, 0, 0, 1, 0, 0, 0, 1))
    m1 = Matrix(3, 4, lambda i, j: i + j)
    assert m1.reshape(
        4, 3) == Matrix(((0, 1, 2), (3, 1, 2), (3, 4, 2), (3, 4, 5)))
    assert m1.reshape(2, 6) == Matrix(((0, 1, 2, 3, 1, 2), (3, 4, 2, 3, 4, 5)))


def test_reshape():
    arr1d = coo_array([1, 0, 3])
    assert arr1d.shape == (3,)

    col_vec = arr1d.reshape((3, 1))
    assert col_vec.shape == (3, 1)
    assert_equal(col_vec.toarray(), np.array([[1], [0], [3]]))

    row_vec = arr1d.reshape((1, 3))
    assert row_vec.shape == (1, 3)
    assert_equal(row_vec.toarray(), np.array([[1, 0, 3]]))

    # attempting invalid reshape
    with pytest.raises(ValueError, match="cannot reshape array"):
        arr1d.reshape((3,3))

    # attempting reshape with a size 0 dimension
    with pytest.raises(ValueError, match="cannot reshape array"):
        arr1d.reshape((3,0))

    arr2d = coo_array([[1, 2, 0], [0, 0, 3]])
    assert arr2d.shape == (2, 3)

    flat = arr2d.reshape((6,))
    assert flat.shape == (6,)
    assert_equal(flat.toarray(), np.array([1, 2, 0, 0, 0, 3]))

    # 2d to 3d
    to_3d_arr = arr2d.reshape((2, 3, 1))
    assert to_3d_arr.shape == (2, 3, 1)
    assert_equal(to_3d_arr.toarray(), np.array([[[1], [2], [0]], [[0], [0], [3]]]))

    # attempting invalid reshape
    with pytest.raises(ValueError, match="cannot reshape array"):
        arr2d.reshape((1,3))

