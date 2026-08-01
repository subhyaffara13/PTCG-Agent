
def test_getitem():
    for ArrayType in [ImmutableDenseNDimArray, ImmutableSparseNDimArray]:
        array = ArrayType(range(24)).reshape(2, 3, 4)
        assert array.tolist() == [[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]], [[12, 13, 14, 15], [16, 17, 18, 19], [20, 21, 22, 23]]]
        assert array[0] == ArrayType([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
        assert array[0, 0] == ArrayType([0, 1, 2, 3])
        value = 0
        for i in range(2):
            for j in range(3):
                for k in range(4):
                    assert array[i, j, k] == value
                    value += 1

    raises(ValueError, lambda: array[3, 4, 5])
    raises(ValueError, lambda: array[3, 4, 5, 6])
    raises(ValueError, lambda: array[3, 4, 5, 3:4])


def test_getitem():
    for ArrayType in [MutableDenseNDimArray, MutableSparseNDimArray]:
        array = ArrayType(range(24)).reshape(2, 3, 4)
        assert array.tolist() == [[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]], [[12, 13, 14, 15], [16, 17, 18, 19], [20, 21, 22, 23]]]
        assert array[0] == ArrayType([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
        assert array[0, 0] == ArrayType([0, 1, 2, 3])
        value = 0
        for i in range(2):
            for j in range(3):
                for k in range(4):
                    assert array[i, j, k] == value
                    value += 1

    raises(ValueError, lambda: array[3, 4, 5])
    raises(ValueError, lambda: array[3, 4, 5, 6])
    raises(ValueError, lambda: array[3, 4, 5, 3:4])


def test_getitem():
    a = intervalMembership(True, False)
    assert a[0] is True
    assert a[1] is False
    raises(IndexError, lambda: a[2])


def test_getitem(xp, ndim: int):
    rng = np.random.default_rng(0)
    quat = rng.normal(size=(2, ) + (ndim,) * (ndim - 1) + (4,))
    mat = xp.asarray(Rotation.from_quat(quat).as_matrix())
    r = Rotation.from_matrix(mat)

    xp_assert_close(r[0].as_matrix(), mat[0, ...], atol=1e-15)
    xp_assert_close(r[1].as_matrix(), mat[1, ...], atol=1e-15)
    xp_assert_close(r[:-1].as_matrix(), xp.expand_dims(mat[0, ...], axis=0), atol=1e-15)


def test_getitem(test_frame):
    g = test_frame.groupby("A")

    expected = g.B.apply(lambda x: x.resample("2s").mean())

    result = g.resample("2s").B.mean()
    tm.assert_series_equal(result, expected)

    result = g.B.resample("2s").mean()
    tm.assert_series_equal(result, expected)

    result = g.resample("2s").mean().B
    tm.assert_series_equal(result, expected)


def test_getitem(test_frame):
    r = test_frame.resample("h")
    tm.assert_index_equal(r._selected_obj.columns, test_frame.columns)

    r = test_frame.resample("h")["B"]
    assert r._selected_obj.name == test_frame.columns[1]

    # technically this is allowed
    r = test_frame.resample("h")["A", "B"]
    tm.assert_index_equal(r._selected_obj.columns, test_frame.columns[[0, 1]])

    r = test_frame.resample("h")["A", "B"]
    tm.assert_index_equal(r._selected_obj.columns, test_frame.columns[[0, 1]])


def test_getitem(step):
    frame = DataFrame(np.random.default_rng(2).standard_normal((5, 5)))
    r = frame.rolling(window=5, step=step)
    tm.assert_index_equal(r._selected_obj.columns, frame[::step].columns)

    r = frame.rolling(window=5, step=step)[1]
    assert r._selected_obj.name == frame[::step].columns[1]

    # technically this is allowed
    r = frame.rolling(window=5, step=step)[1, 3]
    tm.assert_index_equal(r._selected_obj.columns, frame[::step].columns[[1, 3]])

    r = frame.rolling(window=5, step=step)[[1, 3]]
    tm.assert_index_equal(r._selected_obj.columns, frame[::step].columns[[1, 3]])


def test_getitem(idx):
    # scalar
    assert idx[2] == ("bar", "one")

    # slice
    result = idx[2:5]
    expected = idx[[2, 3, 4]]
    assert result.equals(expected)

    # boolean
    result = idx[[True, False, True, False, True, True]]
    result2 = idx[np.array([True, False, True, False, True, True])]
    expected = idx[[0, 2, 4, 5]]
    assert result.equals(expected)
    assert result2.equals(expected)

