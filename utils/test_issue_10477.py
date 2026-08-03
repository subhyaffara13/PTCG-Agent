from typing import Union

def test_issue_10477():
    assert solveset((x**2 + 4*x - 3)/x < 2, x, S.Reals) == \
        Union(Interval.open(-oo, -3), Interval.open(0, 1))

