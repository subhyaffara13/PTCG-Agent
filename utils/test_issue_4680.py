
def test_issue_4680():
    N = Symbol('N')
    assert N.subs({"N": 3}) == 3

