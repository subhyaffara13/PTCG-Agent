
def test_issue_18421():
    assert floor(float(0)) is S.Zero
    assert ceiling(float(0)) is S.Zero

