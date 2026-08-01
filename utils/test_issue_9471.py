
def test_issue_9471():
    assert limit(((27**(log(n,3)))/n**3),n,oo) == 1
    assert limit(((27**(log(n,3)+1))/n**3),n,oo) == 27

