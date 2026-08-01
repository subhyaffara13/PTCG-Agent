
def test_indexing_interactions():
    assert (a * IM)[1, 1] == 5*a
    assert (SM + IM)[1, 1] == SM[1, 1] + IM[1, 1]
    assert (SM * IM)[1, 1] == SM[1, 0]*IM[0, 1] + SM[1, 1]*IM[1, 1] + \
        SM[1, 2]*IM[2, 1]

