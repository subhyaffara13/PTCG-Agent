
def test_fillwithbytes(install_temp):
    import checks

    arr = checks.compile_fillwithbyte()
    assert_array_equal(arr, np.ones((1, 2)))

