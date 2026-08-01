
def test_arrayexpr_convert_array_to_matrix_remove_trivial_dims():

    # Tensor Product:
    assert _remove_trivial_dims(_array_tensor_product(a, b)) == (a * b.T, [1, 3])
    assert _remove_trivial_dims(_array_tensor_product(a.T, b)) == (a * b.T, [0, 3])
    assert _remove_trivial_dims(_array_tensor_product(a, b.T)) == (a * b.T, [1, 2])
    assert _remove_trivial_dims(_array_tensor_product(a.T, b.T)) == (a * b.T, [0, 2])

    assert _remove_trivial_dims(_array_tensor_product(I, a.T, b.T)) == (_array_tensor_product(I, a * b.T), [2, 4])
    assert _remove_trivial_dims(_array_tensor_product(a.T, I, b.T)) == (_array_tensor_product(a.T, I, b.T), [])

    assert _remove_trivial_dims(_array_tensor_product(a, I)) == (_array_tensor_product(a, I), [])
    assert _remove_trivial_dims(_array_tensor_product(I, a)) == (_array_tensor_product(I, a), [])

    assert _remove_trivial_dims(_array_tensor_product(a.T, b.T, c, d)) == (
        _array_tensor_product(a * b.T, c * d.T), [0, 2, 5, 7])
    assert _remove_trivial_dims(_array_tensor_product(a.T, I, b.T, c, d, I)) == (
        _array_tensor_product(a.T, I, b*c.T, d, I), [4, 7])

    # Addition:

    cg = ArrayAdd(_array_tensor_product(a, b), _array_tensor_product(c, d))
    assert _remove_trivial_dims(cg) == (a * b.T + c * d.T, [1, 3])

    # Permute Dims:

    cg = PermuteDims(_array_tensor_product(a, b), Permutation(3)(1, 2))
    assert _remove_trivial_dims(cg) == (a * b.T, [2, 3])

    cg = PermuteDims(_array_tensor_product(a, I, b), Permutation(5)(1, 2, 3, 4))
    assert _remove_trivial_dims(cg) == (cg, [])

    cg = PermuteDims(_array_tensor_product(I, b, a), Permutation(5)(1, 2, 4, 5, 3))
    assert _remove_trivial_dims(cg) == (PermuteDims(_array_tensor_product(I, b * a.T), [0, 2, 3, 1]), [4, 5])

    # Diagonal:

    cg = _array_diagonal(_array_tensor_product(M, a), (1, 2))
    assert _remove_trivial_dims(cg) == (cg, [])

    # Contraction:

    cg = _array_contraction(_array_tensor_product(M, a), (1, 2))
    assert _remove_trivial_dims(cg) == (cg, [])

    # A few more cases to test the removal and shift of nested removed axes
    # with array contractions and array diagonals:
    tp = _array_tensor_product(
        OneMatrix(1, 1),
        M,
        x,
        OneMatrix(1, 1),
        Identity(1),
    )

    expr = _array_contraction(tp, (1, 8))
    rexpr, removed = _remove_trivial_dims(expr)
    assert removed == [0, 5, 6, 7]

    expr = _array_contraction(tp, (1, 8), (3, 4))
    rexpr, removed = _remove_trivial_dims(expr)
    assert removed == [0, 3, 4, 5]

    expr = _array_diagonal(tp, (1, 8))
    rexpr, removed = _remove_trivial_dims(expr)
    assert removed == [0, 5, 6, 7, 8]

    expr = _array_diagonal(tp, (1, 8), (3, 4))
    rexpr, removed = _remove_trivial_dims(expr)
    assert removed == [0, 3, 4, 5, 6]

    expr = _array_diagonal(_array_contraction(_array_tensor_product(A, x, I, I1), (1, 2, 5)), (1, 4))
    rexpr, removed = _remove_trivial_dims(expr)
    assert removed == [2, 3]

    cg = _array_diagonal(_array_tensor_product(PermuteDims(_array_tensor_product(x, I1), Permutation(1, 2, 3)), (x.T*x).applyfunc(sqrt)), (2, 4), (3, 5))
    rexpr, removed = _remove_trivial_dims(cg)
    assert removed == [1, 2]

    # Contractions with identity matrices need to be followed by a permutation
    # in order
    cg = _array_contraction(_array_tensor_product(A, B, C, M, I), (1, 8))
    ret, removed = _remove_trivial_dims(cg)
    assert ret == PermuteDims(_array_tensor_product(A, B, C, M), [0, 2, 3, 4, 5, 6, 7, 1])
    assert removed == []

    cg = _array_contraction(_array_tensor_product(A, B, C, M, I), (1, 8), (3, 4))
    ret, removed = _remove_trivial_dims(cg)
    assert ret == PermuteDims(_array_contraction(_array_tensor_product(A, B, C, M), (3, 4)), [0, 2, 3, 4, 5, 1])
    assert removed == []

    # Trivial matrices are sometimes inserted into MatMul expressions:

    cg = _array_tensor_product(b*b.T, a.T*a)
    ret, removed = _remove_trivial_dims(cg)
    assert ret == b*a.T*a*b.T
    assert removed == [2, 3]

    Xs = ArraySymbol("X", (3, 2, k))
    cg = _array_tensor_product(M, Xs, b.T*c, a*a.T, b*b.T, c.T*d)
    ret, removed = _remove_trivial_dims(cg)
    assert ret == _array_tensor_product(M, Xs, a*b.T*c*c.T*d*a.T, b*b.T)
    assert removed == [5, 6, 11, 12]

    cg = _array_diagonal(_array_tensor_product(I, I1, x), (1, 4), (3, 5))
    assert _remove_trivial_dims(cg) == (PermuteDims(_array_diagonal(_array_tensor_product(I, x), (1, 2)), Permutation(1, 2)), [1])

    expr = _array_diagonal(_array_tensor_product(x, I, y), (0, 2))
    assert _remove_trivial_dims(expr) == (PermuteDims(_array_tensor_product(DiagMatrix(x), y), [1, 2, 3, 0]), [0])

    expr = _array_diagonal(_array_tensor_product(x, I, y), (0, 2), (3, 4))
    assert _remove_trivial_dims(expr) == (expr, [])

