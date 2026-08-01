
def test_sympify_yn():
    assert S(15) in myn(3, pi).atoms()
    assert myn(3, pi) == 15/pi**4 - 6/pi**2

