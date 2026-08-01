
def test_npystring_multiple_allocators(install_temp):
    """Check that the cython API can acquire/release multiple vstring allocators."""
    import checks

    dt = np.dtypes.StringDType(na_object=None)
    arr1 = np.array(['abcd', 'b', 'c'], dtype=dt)
    arr2 = np.array(['a', 'b', 'c'], dtype=dt)

    assert checks.npystring_pack_multiple(arr1, arr2) == 0
    assert arr1[0] == "Hello world"
    assert arr1[-1] is None
    assert arr2[0] == "test this"

