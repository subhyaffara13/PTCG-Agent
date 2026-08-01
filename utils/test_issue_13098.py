
def test_issue_13098():
    assert floor(log(S('9.'+'9'*20), 10)) == 0
    assert ceiling(log(S('9.'+'9'*20), 10)) == 1
    assert floor(log(20 - S('9.'+'9'*20), 10)) == 1
    assert ceiling(log(20 - S('9.'+'9'*20), 10)) == 2

