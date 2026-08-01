
def test_issue_2799():
    U = S.UniversalSet
    a = Symbol('a', real=True)
    inf_interval = Interval(a, oo)
    R = S.Reals

    assert U + inf_interval == inf_interval + U
    assert U + R == R + U
    assert R + inf_interval == inf_interval + R

