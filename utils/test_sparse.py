
def test_sparse():
    pytest.importorskip("scipy")
    assert_sparse_equal_ref(m.sparse_r())
    assert_sparse_equal_ref(m.sparse_c())
    assert_sparse_equal_ref(m.sparse_copy_r(m.sparse_r()))
    assert_sparse_equal_ref(m.sparse_copy_c(m.sparse_c()))
    assert_sparse_equal_ref(m.sparse_copy_r(m.sparse_c()))
    assert_sparse_equal_ref(m.sparse_copy_c(m.sparse_r()))


def test_sparse():
    sparse_array = ImmutableSparseNDimArray([0, 0, 0, 1], (2, 2))
    assert len(sparse_array) == 2 * 2
    # dictionary where all data is, only non-zero entries are actually stored:
    assert len(sparse_array._sparse_array) == 1

    assert sparse_array.tolist() == [[0, 0], [0, 1]]

    for i, j in zip(sparse_array, [[0, 0], [0, 1]]):
        assert i == ImmutableSparseNDimArray(j)

    def sparse_assignment():
        sparse_array[0, 0] = 123

    assert len(sparse_array._sparse_array) == 1
    raises(TypeError, sparse_assignment)
    assert len(sparse_array._sparse_array) == 1
    assert sparse_array[0, 0] == 0
    assert sparse_array/0 == ImmutableSparseNDimArray([[S.NaN, S.NaN], [S.NaN, S.ComplexInfinity]], (2, 2))

    # test for large scale sparse array
    # equality test
    assert ImmutableSparseNDimArray.zeros(100000, 200000) == ImmutableSparseNDimArray.zeros(100000, 200000)

    # __mul__ and __rmul__
    a = ImmutableSparseNDimArray({200001: 1}, (100000, 200000))
    assert a * 3 == ImmutableSparseNDimArray({200001: 3}, (100000, 200000))
    assert 3 * a == ImmutableSparseNDimArray({200001: 3}, (100000, 200000))
    assert a * 0 == ImmutableSparseNDimArray({}, (100000, 200000))
    assert 0 * a == ImmutableSparseNDimArray({}, (100000, 200000))

    # __truediv__
    assert a/3 == ImmutableSparseNDimArray({200001: Rational(1, 3)}, (100000, 200000))

    # __neg__
    assert -a == ImmutableSparseNDimArray({200001: -1}, (100000, 200000))


def test_sparse():
    sparse_array = MutableSparseNDimArray([0, 0, 0, 1], (2, 2))
    assert len(sparse_array) == 2 * 2
    # dictionary where all data is, only non-zero entries are actually stored:
    assert len(sparse_array._sparse_array) == 1

    assert sparse_array.tolist() == [[0, 0], [0, 1]]

    for i, j in zip(sparse_array, [[0, 0], [0, 1]]):
        assert i == MutableSparseNDimArray(j)

    sparse_array[0, 0] = 123
    assert len(sparse_array._sparse_array) == 2
    assert sparse_array[0, 0] == 123
    assert sparse_array/0 == MutableSparseNDimArray([[S.ComplexInfinity, S.NaN], [S.NaN, S.ComplexInfinity]], (2, 2))

    # when element in sparse array become zero it will disappear from
    # dictionary
    sparse_array[0, 0] = 0
    assert len(sparse_array._sparse_array) == 1
    sparse_array[1, 1] = 0
    assert len(sparse_array._sparse_array) == 0
    assert sparse_array[0, 0] == 0

    # test for large scale sparse array
    # equality test
    a = MutableSparseNDimArray.zeros(100000, 200000)
    b = MutableSparseNDimArray.zeros(100000, 200000)
    assert a == b
    a[1, 1] = 1
    b[1, 1] = 2
    assert a != b

    # __mul__ and __rmul__
    assert a * 3 == MutableSparseNDimArray({200001: 3}, (100000, 200000))
    assert 3 * a == MutableSparseNDimArray({200001: 3}, (100000, 200000))
    assert a * 0 == MutableSparseNDimArray({}, (100000, 200000))
    assert 0 * a == MutableSparseNDimArray({}, (100000, 200000))

    # __truediv__
    assert a/3 == MutableSparseNDimArray({200001: Rational(1, 3)}, (100000, 200000))

    # __neg__
    assert -a == MutableSparseNDimArray({200001: -1}, (100000, 200000))


def test_sparse():
    M = SparseMatrix(5, 6, {})
    M[2, 2] = 10
    M[1, 2] = 20
    M[1, 3] = 22
    M[0, 3] = 30
    M[3, 0] = x*y
    assert julia_code(M) == (
        "sparse([4, 2, 3, 1, 2], [1, 3, 3, 4, 4], [x .* y, 20, 10, 30, 22], 5, 6)"
    )


def test_sparse():
    M = SparseMatrix(5, 6, {})
    M[2, 2] = 10
    M[1, 2] = 20
    M[1, 3] = 22
    M[0, 3] = 30
    M[3, 0] = x * y
    assert maple_code(M) == \
           'Matrix([[0, 0, 0, 30, 0, 0],' \
           ' [0, 0, 20, 22, 0, 0],' \
           ' [0, 0, 10, 0, 0, 0],' \
           ' [x*y, 0, 0, 0, 0, 0],' \
           ' [0, 0, 0, 0, 0, 0]], ' \
           'storage = sparse)'


def test_sparse():
    M = SparseMatrix(5, 6, {})
    M[2, 2] = 10
    M[1, 2] = 20
    M[1, 3] = 22
    M[0, 3] = 30
    M[3, 0] = x*y
    assert mcode(M) == (
        "sparse([4 2 3 1 2], [1 3 3 4 4], [x.*y 20 10 30 22], 5, 6)"
    )


def test_sparse(string: str) -> None:
    np = pytest.importorskip("numpy")
    sparse = pytest.importorskip("sparse")

    views = build_views(string)

    # sparsify views so they don't become dense during contraction
    for view in views:
        np.random.seed(42)
        mask = np.random.choice([False, True], view.shape, True, [0.05, 0.95])
        view[mask] = 0

    ein = contract(string, *views, optimize=False, use_blas=False)
    shps = [v.shape for v in views]
    expr = contract_expression(string, *shps, optimize=True)

    # test non-conversion mode
    sparse_views = [sparse.COO.from_numpy(x) for x in views]
    sparse_opt = expr(*sparse_views)

    # If the expression returns a float, stop here
    if not ein.shape:
        assert pytest.approx(ein) == 0.0
        return

    # check type is maintained when not using numpy arrays
    assert isinstance(sparse_opt, sparse.COO)
    assert np.allclose(ein, sparse_opt.todense())

    # try raw contract
    sparse_opt = contract(string, *sparse_views)
    assert isinstance(sparse_opt, sparse.COO)
    assert np.allclose(ein, sparse_opt.todense())

