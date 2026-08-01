
def test_Domain_map():
    seq = ZZ.map([1, 2, 3, 4])

    assert all(ZZ.of_type(elt) for elt in seq)

    seq = ZZ.map([[1, 2, 3, 4]])

    assert all(ZZ.of_type(elt) for elt in seq[0]) and len(seq) == 1

