
def test_fuzzy_xor():
    assert fuzzy_xor((None,)) is None
    assert fuzzy_xor((None, True)) is None
    assert fuzzy_xor((None, False)) is None
    assert fuzzy_xor((True, False)) is True
    assert fuzzy_xor((True, True)) is False
    assert fuzzy_xor((True, True, False)) is False
    assert fuzzy_xor((True, True, False, True)) is True

