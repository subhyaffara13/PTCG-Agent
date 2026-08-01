
def test_nth_root():
    R, x, y = puiseux_ring('x, y', QQ)
    assert rs_nth_root(1 + x**2*y, 4, x, 10) == -77*x**8*y**4/2048 + \
        7*x**6*y**3/128 - 3*x**4*y**2/32 + x**2*y/4 + 1
    assert rs_nth_root(1 + x*y + x**2*y**3, 3, x, 5) == -x**4*y**6/9 + \
        5*x**4*y**5/27 - 10*x**4*y**4/243 - 2*x**3*y**4/9 + 5*x**3*y**3/81 + \
        x**2*y**3/3 - x**2*y**2/9 + x*y/3 + 1
    assert rs_nth_root(8*x, 3, x, 3) == 2*x**QQ(1, 3)
    assert rs_nth_root(8*x + x**2 + x**3, 3, x, 3) == x**QQ(4,3)/12 + 2*x**QQ(1,3)
    r = rs_nth_root(8*x + x**2*y + x**3, 3, x, 4)
    assert r == -x**QQ(7,3)*y**2/288 + x**QQ(7,3)/12 + x**QQ(4,3)*y/12 + 2*x**QQ(1,3)

    # Constant term in series
    a = symbols('a')
    R, x, y = puiseux_ring('x, y', EX)
    assert rs_nth_root(x + EX(a), 3, x, 4) == EX(5/(81*a**QQ(8, 3)))*x**3 - \
        EX(1/(9*a**QQ(5, 3)))*x**2 + EX(1/(3*a**QQ(2, 3)))*x + EX(a**QQ(1, 3))
    assert rs_nth_root(x**QQ(2, 3) + x**2*y + 5, 2, x, 3) == -EX(sqrt(5)/100)*\
        x**QQ(8, 3)*y - EX(sqrt(5)/16000)*x**QQ(8, 3) + EX(sqrt(5)/10)*x**2*y + \
        EX(sqrt(5)/2000)*x**2 - EX(sqrt(5)/200)*x**QQ(4, 3) + \
        EX(sqrt(5)/10)*x**QQ(2, 3) + EX(sqrt(5))

