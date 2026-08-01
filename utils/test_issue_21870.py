
def test_issue_21870():
    a0 = ImmutableDenseNDimArray(0)
    assert a0.rank() == 0
    a1 = ImmutableDenseNDimArray(a0)
    assert a1.rank() == 0

