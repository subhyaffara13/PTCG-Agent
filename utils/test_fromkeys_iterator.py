
def test_fromkeys_iterator():
    it = ((a, a % 2) for a in range(4))
    Xdok = dok_array.fromkeys(it)
    X = [[1, 0], [0, 1], [1, 0], [0, 1]]
    assert_equal(Xdok.toarray(), X)

