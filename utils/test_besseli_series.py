
def test_besseli_series():
    assert besseli(0, x).series(x) == 1 + x**2/4 + x**4/64 + O(x**6)
    assert besseli(0, x**(1.1)).series(x) == 1 + x**4.4/64 + x**2.2/4 + O(x**6)
    assert besseli(0, x**2 + x).series(x) == 1 + x**2/4 + x**3/2 + 17*x**4/64 + \
        x**5/16 + O(x**6)
    assert besseli(0, sqrt(x) + x).series(x, n=4) == 1 + x/4 + 17*x**2/64 + \
        217*x**3/2304 + x**(S(3)/2)/2 + x**(S(5)/2)/16 + 25*x**(S(7)/2)/384 + O(x**4)
    assert besseli(0, x/(1 - x)).series(x) == 1 + x**2/4 + x**3/2 + 49*x**4/64 + \
        17*x**5/16 + O(x**6)
    assert besseli(0, log(1 + x)).series(x) == 1 + x**2/4 - x**3/4 + 47*x**4/192 - \
        23*x**5/96 + O(x**6)
    assert besseli(1, sin(x)).series(x) == x/2 - x**3/48 - 47*x**5/1920 + O(x**6)
    assert besseli(1, 2*sqrt(x)).series(x) == sqrt(x) + x**(S(3)/2)/2 + x**(S(5)/2)/12 + \
        x**(S(7)/2)/144 + x**(S(9)/2)/2880 + x**(S(11)/2)/86400 + O(x**6)
    assert besseli(-2, sin(x)).series(x, n=4) == besseli(2, sin(x)).series(x, n=4)

    #test for aseries
    assert besseli(0,x).series(x, oo, n=4) == sqrt(2)*(sqrt(1/x) - (1/x)**(S(3)/2)/8 - \
        3*(1/x)**(S(5)/2)/128 - 15*(1/x)**(S(7)/2)/1024 + O((1/x)**(S(9)/2), (x, oo)))*exp(x)/(2*sqrt(pi))
    assert besseli(0,x).series(x,-oo, n=4) == sqrt(2)*(sqrt(-1/x) - (-1/x)**(S(3)/2)/8 - 3*(-1/x)**(S(5)/2)/128 - \
        15*(-1/x)**(S(7)/2)/1024 + O((-1/x)**(S(9)/2), (x, -oo)))*exp(-x)/(2*sqrt(pi))

