
def test_function__eval_nseries():
    n = Symbol('n')

    assert sin(x)._eval_nseries(x, 2, None) == x + O(x**2)
    assert sin(x + 1)._eval_nseries(x, 2, None) == x*cos(1) + sin(1) + O(x**2)
    assert sin(pi*(1 - x))._eval_nseries(x, 2, None) == pi*x + O(x**2)
    assert acos(1 - x**2)._eval_nseries(x, 2, None) == sqrt(2)*sqrt(x**2) + O(x**2)
    assert polygamma(n, x + 1)._eval_nseries(x, 2, None) == \
        polygamma(n, 1) + polygamma(n + 1, 1)*x + O(x**2)
    raises(PoleError, lambda: sin(1/x)._eval_nseries(x, 2, None))
    assert acos(1 - x)._eval_nseries(x, 2, None) == sqrt(2)*sqrt(x) + sqrt(2)*x**(S(3)/2)/12 + O(x**2)
    assert acos(1 + x)._eval_nseries(x, 2, None) == sqrt(2)*sqrt(-x) + sqrt(2)*(-x)**(S(3)/2)/12 + O(x**2)
    assert loggamma(1/x)._eval_nseries(x, 0, None) == \
        log(x)/2 - log(x)/x - 1/x + O(1, x)
    assert loggamma(log(1/x)).nseries(x, n=1, logx=y) == loggamma(-y)

    # issue 6725:
    assert expint(Rational(3, 2), -x)._eval_nseries(x, 5, None) == \
        2 - 2*x - x**2/3 - x**3/15 - x**4/84 - 2*I*sqrt(pi)*sqrt(x) + O(x**5)
    assert sin(sqrt(x))._eval_nseries(x, 3, None) == \
        sqrt(x) - x**Rational(3, 2)/6 + x**Rational(5, 2)/120 + O(x**3)

    # issue 19065:
    s1 = f(x,y).series(y, n=2)
    assert {i.name for i in s1.atoms(Symbol)} == {'x', 'xi', 'y'}
    xi = Symbol('xi')
    s2 = f(xi, y).series(y, n=2)
    assert {i.name for i in s2.atoms(Symbol)} == {'xi', 'xi0', 'y'}

