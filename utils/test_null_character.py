
def test_null_character():
    # Basic tests to check that the NUL character is not special:
    res = np.loadtxt(["1\0002\0003\n", "4\0005\0006"], delimiter="\000")
    assert_array_equal(res, [[1, 2, 3], [4, 5, 6]])

    # Also not as part of a field (avoid unicode/arrays as unicode strips \0)
    res = np.loadtxt(["1\000,2\000,3\n", "4\000,5\000,6"],
                     delimiter=",", dtype=object)
    assert res.tolist() == [["1\000", "2\000", "3"], ["4\000", "5\000", "6"]]

