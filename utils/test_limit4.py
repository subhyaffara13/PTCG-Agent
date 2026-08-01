
def test_limit4():
    #issue 3463
    assert gruntz((3**x + 5**x)**(1/x), x, oo) == 5
    #issue 3463
    assert gruntz((3**(1/x) + 5**(1/x))**x, x, 0) == 5

