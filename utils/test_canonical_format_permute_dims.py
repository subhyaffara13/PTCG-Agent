
def test_canonical_format_permute_dims():
    A = coo_array([[2, 0, 1], [3, 5, 0]])
    # identity axes keep has_canoncial_format True after permute_dims.
    assert construct.permute_dims(A, axes=(0, 1)).has_canonical_format is True
    assert construct.permute_dims(A, axes=[0, 1]).has_canonical_format is True
    # order changes set has_canonical_format to False
    assert construct.permute_dims(A, axes=[1, 0]).has_canonical_format is False

