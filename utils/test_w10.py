
def test_W10():
    # integrate(1/[1 + x + x^2 + ... + x^(2 n)], x = -infinity..infinity) =
    #        2 pi/(2 n + 1) [1 + cos(pi/[2 n + 1])] csc(2 pi/[2 n + 1])
    # [Levinson and Redheffer, p. 255] => 2 pi/5 [1 + cos(pi/5)] csc(2 pi/5) */
    r1 = integrate(x/(1 + x + x**2 + x**4), (x, -oo, oo))
    r2 = r1.doit()
    assert r2 == 2*pi*(sqrt(5)/4 + 5/4)*csc(pi*R(2, 5))/5

