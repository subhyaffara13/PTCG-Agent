from typing import Union

def test_issue_25768():
    assert dumeq(solveset_real(sin(x) - S.Half, x), Union(
        ImageSet(Lambda(n, pi*2*n + pi/6), S.Integers),
        ImageSet(Lambda(n, pi*2*n + pi*5/6), S.Integers)))
    n1 = solveset_real(sin(x) - 0.5, x).n(5)
    n2 = solveset_real(sin(x) - S.Half, x).n(5)
    # help pass despite fp differences
    eq = [i.replace(
        lambda x:x.is_Float,
        lambda x:Rational(x).limit_denominator(1000)) for i in (n1, n2)]
    assert dumeq(*eq),(n1,n2)

