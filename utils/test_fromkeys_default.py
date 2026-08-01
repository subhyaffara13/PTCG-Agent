
def test_fromkeys_default():
    # test with default value
    edges = [(0, 2), (1, 0), (2, 1)]
    Xdok = dok_array.fromkeys(edges)
    X = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
    assert_equal(Xdok.toarray(), X)

