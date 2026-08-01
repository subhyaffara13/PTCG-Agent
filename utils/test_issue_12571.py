
def test_issue_12571():
    assert limit(-LambertW(-log(x))/log(x), x, 1) == 1

