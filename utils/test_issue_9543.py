
def test_issue_9543():
    assert ImageSet(Lambda(x, x**2), S.Naturals).is_subset(S.Reals)

