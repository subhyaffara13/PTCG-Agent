
def test_puiseux2():
    R, y = ring('y', QQ)
    S, x = puiseux_ring('x', R.to_domain())

    p = x + x**QQ(1,5)*y
    r = rs_atan(p, x, 3)
    assert r == (y**13/13 + y**8 + 2*y**3)*x**QQ(13,5) - (y**11/11 + y**6 +
        y)*x**QQ(11,5) + (y**9/9 + y**4)*x**QQ(9,5) - (y**7/7 +
        y**2)*x**QQ(7,5) + (y**5/5 + 1)*x - y**3*x**QQ(3,5)/3 + y*x**QQ(1,5)

