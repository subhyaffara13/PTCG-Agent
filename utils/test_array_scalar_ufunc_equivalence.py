
def test_array_scalar_ufunc_equivalence(op, arr1, arr2):
    """
    This is a thorough test attempting to cover important promotion paths
    and ensuring that arrays and scalars stay as aligned as possible.
    However, if it creates troubles, it should maybe just be removed.
    """
    check_ufunc_scalar_equivalence(op, arr1, arr2)

