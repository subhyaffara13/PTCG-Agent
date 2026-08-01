
def test_conjuncts():
    assert conjuncts(A & B & C) == {A, B, C}
    assert conjuncts((A | B) & C) == {A | B, C}
    assert conjuncts(A) == {A}
    assert conjuncts(True) == {True}
    assert conjuncts(False) == {False}

