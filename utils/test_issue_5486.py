
def test_issue_5486():
    assert not cos(sqrt(0.5 + I)).n().is_Function

