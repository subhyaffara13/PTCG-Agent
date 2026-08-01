
def test_cot_subs():
    assert cot(x).subs(cot(x), y) == y
    assert cot(x).subs(x, y) == cot(y)
    assert cot(x).subs(x, 0) is zoo
    assert cot(x).subs(x, S.Pi) is zoo

