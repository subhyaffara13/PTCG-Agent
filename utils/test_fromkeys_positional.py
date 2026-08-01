
def test_fromkeys_positional():
    # test with positional value
    edges = [(0, 2), (1, 0), (2, 1)]
    Xdok = dok_array.fromkeys(edges, -1)
    X = [[0, 0, -1], [-1, 0, 0], [0, -1, 0]]
    assert_equal(Xdok.toarray(), X)

