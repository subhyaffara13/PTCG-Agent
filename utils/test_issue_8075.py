
def test_issue_8075():
    raises(InconsistentAssumptions, lambda: Dummy(zero=True, finite=False))
    raises(InconsistentAssumptions, lambda: Dummy(zero=True, infinite=True))

