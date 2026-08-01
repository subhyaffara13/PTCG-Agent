
def test_npystring_pack(install_temp):
    """Check that the cython API can write to a vstring array."""
    import checks

    arr = np.array(['a', 'b', 'c'], dtype='T')
    assert checks.npystring_pack(arr) == 0

    # checks.npystring_pack writes to the beginning of the array
    assert arr[0] == "Hello world"

