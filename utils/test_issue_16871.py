
def test_issue_16871():
    assert ImageSet(Lambda(x, x), FiniteSet(1)) == {1}
    assert ImageSet(Lambda(x, x - 3), S.Integers
        ).intersection(S.Integers) is S.Integers

