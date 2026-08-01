
def test_npystring_load(install_temp):
    """Check that the cython API can load strings from a vstring array."""
    import checks

    arr = np.array(['abcd', 'b', 'c'], dtype='T')
    result = checks.npystring_load(arr)
    assert result == 'abcd'

