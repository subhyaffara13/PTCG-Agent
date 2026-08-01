
def test_issue_4814():
    assert gruntz((x + 1)**(1/log(x + 1)), x, oo) == E

