
def test_arrayexpr_contraction_construction():

    cg = _array_contraction(A)
    assert cg == A

    cg = _array_contraction(_array_tensor_product(A, B), (1, 0))
    assert cg == _array_contraction(_array_tensor_product(A, B), (0, 1))

    cg = _array_contraction(_array_tensor_product(M, N), (0, 1))
    indtup = cg._get_contraction_tuples()
    assert indtup == [[(0, 0), (0, 1)]]
    assert cg._contraction_tuples_to_contraction_indices(cg.expr, indtup) == [(0, 1)]

    cg = _array_contraction(_array_tensor_product(M, N), (1, 2))
    indtup = cg._get_contraction_tuples()
    assert indtup == [[(0, 1), (1, 0)]]
    assert cg._contraction_tuples_to_contraction_indices(cg.expr, indtup) == [(1, 2)]

    cg = _array_contraction(_array_tensor_product(M, M, N), (1, 4), (2, 5))
    indtup = cg._get_contraction_tuples()
    assert indtup == [[(0, 0), (1, 1)], [(0, 1), (2, 0)]]
    assert cg._contraction_tuples_to_contraction_indices(cg.expr, indtup) == [(0, 3), (1, 4)]

    # Test removal of trivial contraction:
    assert _array_contraction(a, (1,)) == a
    assert _array_contraction(
        _array_tensor_product(a, b), (0, 2), (1,), (3,)) == _array_contraction(
        _array_tensor_product(a, b), (0, 2))

