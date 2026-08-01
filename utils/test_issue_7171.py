
def test_issue_7171():
    assert sin(x).rewrite(sqrt) == sin(x)
    assert sin(x).rewrite(pow) == sin(x)

