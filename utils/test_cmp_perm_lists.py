
def test_cmp_perm_lists():
    S = SymmetricGroup(4)
    els = list(S.generate_dimino())
    other = els.copy()
    shuffle(other)
    assert _cmp_perm_lists(els, other) is True

