
def test_check_cycles_alt_sym():
    perm1 = Permutation([[0, 1, 2, 3, 4, 5, 6], [7], [8], [9]])
    perm2 = Permutation([[0, 1, 2, 3, 4, 5], [6, 7, 8, 9]])
    perm3 = Permutation([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
    assert _check_cycles_alt_sym(perm1) is True
    assert _check_cycles_alt_sym(perm2) is False
    assert _check_cycles_alt_sym(perm3) is False

