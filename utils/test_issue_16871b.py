
def test_issue_16871b():
    assert ImageSet(Lambda(x, x - 3), S.Integers).is_subset(S.Integers)

