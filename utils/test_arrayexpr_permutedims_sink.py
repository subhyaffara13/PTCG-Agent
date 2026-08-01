
def test_arrayexpr_permutedims_sink():

    cg = _permute_dims(_array_tensor_product(M, N), [0, 1, 3, 2], nest_permutation=False)
    sunk = nest_permutation(cg)
    assert sunk == _array_tensor_product(M, _permute_dims(N, [1, 0]))

    cg = _permute_dims(_array_tensor_product(M, N), [1, 0, 3, 2], nest_permutation=False)
    sunk = nest_permutation(cg)
    assert sunk == _array_tensor_product(_permute_dims(M, [1, 0]), _permute_dims(N, [1, 0]))

    cg = _permute_dims(_array_tensor_product(M, N), [3, 2, 1, 0], nest_permutation=False)
    sunk = nest_permutation(cg)
    assert sunk == _array_tensor_product(_permute_dims(N, [1, 0]), _permute_dims(M, [1, 0]))

    cg = _permute_dims(_array_contraction(_array_tensor_product(M, N), (1, 2)), [1, 0], nest_permutation=False)
    sunk = nest_permutation(cg)
    assert sunk == _array_contraction(_permute_dims(_array_tensor_product(M, N), [[0, 3]]), (1, 2))

    cg = _permute_dims(_array_tensor_product(M, N), [1, 0, 3, 2], nest_permutation=False)
    sunk = nest_permutation(cg)
    assert sunk == _array_tensor_product(_permute_dims(M, [1, 0]), _permute_dims(N, [1, 0]))

    cg = _permute_dims(_array_contraction(_array_tensor_product(M, N, P), (1, 2), (3, 4)), [1, 0], nest_permutation=False)
    sunk = nest_permutation(cg)
    assert sunk == _array_contraction(_permute_dims(_array_tensor_product(M, N, P), [[0, 5]]), (1, 2), (3, 4))

