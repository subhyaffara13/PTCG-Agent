
def test_guard_against_indeterminate_evaluation():
    eq = x**y
    assert eq.subs([(x, 1), (y, oo)]) == 1  # because 1**y == 1
    assert eq.subs([(y, oo), (x, 1)]) is S.NaN
    assert eq.subs({x: 1, y: oo}) is S.NaN
    assert eq.subs([(x, 1), (y, oo)], simultaneous=True) is S.NaN

