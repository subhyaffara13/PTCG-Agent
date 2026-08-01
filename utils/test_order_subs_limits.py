
def test_order_subs_limits():
    # issue 3333
    assert (1 + Order(x)).subs(x, 1/x) == 1 + Order(1/x, (x, oo))
    assert (1 + Order(x)).limit(x, 0) == 1
    # issue 5769
    assert ((x + Order(x**2))/x).limit(x, 0) == 1

    assert Order(x**2).subs(x, y - 1) == Order((y - 1)**2, (y, 1))
    assert Order(10*x**2, (x, 2)).subs(x, y - 1) == Order(1, (y, 3))

    #issue 19120
    assert O(x).subs(x, O(x)) == O(x)
    assert O(x**2).subs(x, x + O(x)) == O(x**2)
    assert O(x, (x, oo)).subs(x, O(x, (x, oo))) == O(x, (x, oo))
    assert O(x**2, (x, oo)).subs(x, x + O(x, (x, oo))) == O(x**2, (x, oo))
    assert (x + O(x**2)).subs(x, x + O(x**2)) == x + O(x**2)
    assert (x**2 + O(x**2) + 1/x**2).subs(x, x + O(x**2)) == (x + O(x**2))**(-2) + O(x**2)
    assert (x**2 + O(x**2) + 1).subs(x, x + O(x**2)) == 1 + O(x**2)
    assert O(x, (x, oo)).subs(x, x + O(x**2, (x, oo))) == O(x**2, (x, oo))
    assert sin(x).series(n=8).subs(x,sin(x).series(n=8)).expand() == x - x**3/3 + x**5/10 - 8*x**7/315 + O(x**8)
    assert cos(x).series(n=8).subs(x,sin(x).series(n=8)).expand() == 1 - x**2/2 + 5*x**4/24 - 37*x**6/720 + O(x**8)
    assert O(x).subs(x, O(1/x, (x, oo))) == O(1/x, (x, oo))

