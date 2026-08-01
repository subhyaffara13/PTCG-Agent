
def test_fuzzy_not():
    assert fuzzy_not(T) == F
    assert fuzzy_not(F) == T
    assert fuzzy_not(U) == U

