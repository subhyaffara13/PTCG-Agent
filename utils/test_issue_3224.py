
def test_issue_3224():
    f = sqrt(1 - sqrt(y))
    assert f.nseries(y, 0, 2) == 1 - sqrt(y)/2 - y/8 - sqrt(y)**3/16 + O(y**2)

