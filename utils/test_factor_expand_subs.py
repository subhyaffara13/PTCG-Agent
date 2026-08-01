
def test_factor_expand_subs():
    # test factoring
    assert Sum(4 * x, (x, 1, y)).factor() == 4 * Sum(x, (x, 1, y))
    assert Sum(x * a, (x, 1, y)).factor() == a * Sum(x, (x, 1, y))
    assert Sum(4 * x * a, (x, 1, y)).factor() == 4 * a * Sum(x, (x, 1, y))
    assert Sum(4 * x * y, (x, 1, y)).factor() == 4 * y * Sum(x, (x, 1, y))

    # test expand
    _x = Symbol('x', zero=False)
    assert Sum(x+1,(x,1,y)).expand() == Sum(x,(x,1,y)) + Sum(1,(x,1,y))
    assert Sum(x+a*x**2,(x,1,y)).expand() == Sum(x,(x,1,y)) + Sum(a*x**2,(x,1,y))
    assert Sum(_x**(n + 1)*(n + 1), (n, -1, oo)).expand() \
        == Sum(n*_x*_x**n + _x*_x**n, (n, -1, oo))
    assert Sum(x**(n + 1)*(n + 1), (n, -1, oo)).expand(power_exp=False) \
        == Sum(n*x**(n + 1) + x**(n + 1), (n, -1, oo))
    assert Sum(x**(n + 1)*(n + 1), (n, -1, oo)).expand(force=True) \
           == Sum(x*x**n, (n, -1, oo)) + Sum(n*x*x**n, (n, -1, oo))
    assert Sum(a*n+a*n**2,(n,0,4)).expand() \
        == Sum(a*n,(n,0,4)) + Sum(a*n**2,(n,0,4))
    assert Sum(_x**a*_x**n,(x,0,3)) \
        == Sum(_x**(a+n),(x,0,3)).expand(power_exp=True)
    _a, _n = symbols('a n', positive=True)
    assert Sum(x**(_a+_n),(x,0,3)).expand(power_exp=True) \
        == Sum(x**_a*x**_n, (x, 0, 3))
    assert Sum(x**(_a-_n),(x,0,3)).expand(power_exp=True) \
        == Sum(x**(_a-_n),(x,0,3)).expand(power_exp=False)

    # test subs
    assert Sum(1/(1+a*x**2),(x,0,3)).subs([(a,3)]) == Sum(1/(1+3*x**2),(x,0,3))
    assert Sum(x*y,(x,0,y),(y,0,x)).subs([(x,3)]) == Sum(x*y,(x,0,y),(y,0,3))
    assert Sum(x,(x,1,10)).subs([(x,y-2)]) == Sum(x,(x,1,10))
    assert Sum(1/x,(x,1,10)).subs([(x,(3+n)**3)]) == Sum(1/x,(x,1,10))
    assert Sum(1/x,(x,1,10)).subs([(x,3*x-2)]) == Sum(1/x,(x,1,10))

