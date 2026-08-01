
def test_issue_10024():
    x = Dummy('x')
    assert Mod(x, 2*pi).is_zero is None

