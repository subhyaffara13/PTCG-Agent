
def test_arrayexpr_array_wrong_permutation_size():
    cg = _array_tensor_product(M, N)
    raises(ValueError, lambda: _permute_dims(cg, [1, 0]))
    raises(ValueError, lambda: _permute_dims(cg, [1, 0, 2, 3, 5, 4]))

