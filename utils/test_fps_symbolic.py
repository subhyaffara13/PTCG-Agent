
def test_fps_symbolic():
    f = x**n*sin(x**2)
    assert fps(f, x).truncate(8) == x**(n + 2) - x**(n + 6)/6 + O(x**(n + 8), x)

    f = x**n*log(1 + x)
    fp = fps(f, x)
    k = fp.ak.variables[0]
    assert fp.infinite == \
        Sum((-(-1)**(-k)*x**(k + n))/k, (k, 1, oo))

    f = (x - 2)**n*log(1 + x)
    assert fps(f, x, 2).truncate() == \
        ((x - 2)**n*log(3) + (x - 2)**(n + 1)/3 - (x - 2)**(n + 2)/18 + (x - 2)**(n + 3)/81 -
         (x - 2)**(n + 4)/324 + (x - 2)**(n + 5)/1215 + O((x - 2)**(n + 6), (x, 2)))

    f = x**(n - 2)*cos(x)
    assert fps(f, x).truncate() == \
        (x**(n - 2) - x**n/2 + x**(n + 2)/24 + O(x**(n + 4), x))

    f = x**(n - 2)*sin(x) + x**n*exp(x)
    assert fps(f, x).truncate() == \
        (x**(n - 1) + x**(n + 1) + x**(n + 2)/2 + x**n +
         x**(n + 4)/24 + x**(n + 5)/60 + O(x**(n + 6), x))

    f = x**n*atan(x)
    assert fps(f, x, oo).truncate() == \
        (-x**(n - 5)/5 + x**(n - 3)/3 + x**n*(pi/2 - 1/x) +
         O((1/x)**(-n)/x**6, (x, oo)))

    f = x**(n/2)*cos(x)
    assert fps(f, x).truncate() == \
        x**(n/2) - x**(n/2 + 2)/2 + x**(n/2 + 4)/24 + O(x**(n/2 + 6), x)

    f = x**(n + m)*sin(x)
    assert fps(f, x).truncate() == \
        x**(m + n + 1) - x**(m + n + 3)/6 + x**(m + n + 5)/120 + O(x**(m + n + 6), x)

