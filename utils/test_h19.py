
def test_H19():
    a = symbols('a')
    # The idea is to let a**2 == 2, then solve 1/(a-1). Answer is a+1")
    assert Poly(a - 1).invert(Poly(a**2 - 2)) == a + 1

