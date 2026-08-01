
def test_issue_25115():
    cond = Contains(x, S.Integers)
    # Previously this raised an exception:
    assert simplify_logic(cond) == cond

