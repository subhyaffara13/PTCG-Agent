
def test_npystring_allocators_other_dtype(install_temp):
    """Check that allocators for non-StringDType arrays is NULL."""
    import checks

    arr1 = np.array([1, 2, 3], dtype='i')
    arr2 = np.array([4, 5, 6], dtype='i')

    assert checks.npystring_allocators_other_types(arr1, arr2) == 0

