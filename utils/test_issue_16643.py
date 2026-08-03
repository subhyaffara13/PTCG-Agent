from typing import Union

def test_issue_16643():
    n = Dummy('n')
    assert solveset(x**2*sin(x), x).dummy_eq(Union(ImageSet(Lambda(n, 2*n*pi + pi), S.Integers),
                                                   ImageSet(Lambda(n, 2*n*pi), S.Integers)))

