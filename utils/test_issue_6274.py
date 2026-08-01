
def test_issue_6274():
    assert Sum(x, (x, 1, 0)).doit() == 0
    assert NS(Sum(x, (x, 1, 0))) == '0'
    assert Sum(n, (n, 10, 5)).doit() == -30
    assert NS(Sum(n, (n, 10, 5))) == '-30.0000000000000'

