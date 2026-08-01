
def test_issue_9954():
    assert isolve(x**2 >= 0, x, relational=False) == S.Reals
    assert isolve(x**2 >= 0, x, relational=True) == S.Reals.as_relational(x)
    assert isolve(x**2 < 0, x, relational=False) == S.EmptySet
    assert isolve(x**2 < 0, x, relational=True) == S.EmptySet.as_relational(x)

