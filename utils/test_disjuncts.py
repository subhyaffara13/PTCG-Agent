
def test_disjuncts():
    assert disjuncts(A | B | C) == {A, B, C}
    assert disjuncts((A | B) & C) == {(A | B) & C}
    assert disjuncts(A) == {A}
    assert disjuncts(True) == {True}
    assert disjuncts(False) == {False}

