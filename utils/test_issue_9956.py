from typing import Union

def test_issue_9956():
    assert Union(Interval(-oo, oo), FiniteSet(1)) == Interval(-oo, oo)
    assert Interval(-oo, oo).contains(1) is S.true

