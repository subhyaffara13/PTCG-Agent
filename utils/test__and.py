
def test_And():
    args = [(True, True), (True, False), (True, None)]
    assert And(*args) == (True, False)

    args = [(False, True), (None, None), (True, True)]
    assert And(*args) == (False, None)


def test_And():
    assert And() is true
    assert And(A) == A
    assert And(True) is true
    assert And(False) is false
    assert And(True, True) is true
    assert And(True, False) is false
    assert And(False, False) is false
    assert And(True, A) == A
    assert And(False, A) is false
    assert And(True, True, True) is true
    assert And(True, True, A) == A
    assert And(True, False, A) is false
    assert And(1, A) == A
    raises(TypeError, lambda: And(2, A))
    assert And(A < 1, A >= 1) is false
    e = A > 1
    assert And(e, e.canonical) == e.canonical
    g, l, ge, le = A > B, B < A, A >= B, B <= A
    assert And(g, l, ge, le) == And(ge, g)
    assert {And(*i) for i in permutations((l, g, le, ge))} == {And(ge, g)}
    assert And(And(Eq(a, 0), Eq(b, 0)), And(Ne(a, 0), Eq(c, 0))) is false

