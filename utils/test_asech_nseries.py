
def test_asech_nseries():
    x = Symbol('x')
    # Tests concerning branch points
    assert asech(x + 1)._eval_nseries(x, 4, None) == sqrt(2)*sqrt(-x) + 5*sqrt(2)*(-x)**(S(3)/2)/12 + \
    43*sqrt(2)*(-x)**(S(5)/2)/160 + 177*sqrt(2)*(-x)**(S(7)/2)/896 + O(x**4)
    # Tests concerning points lying on branch cuts
    assert asech(x - 1)._eval_nseries(x, 4, None) == I*pi + sqrt(2)*sqrt(x) + \
    5*sqrt(2)*x**(S(3)/2)/12 + 43*sqrt(2)*x**(S(5)/2)/160 + 177*sqrt(2)*x**(S(7)/2)/896 + O(x**4)
    assert asech(I*x + 3)._eval_nseries(x, 4, None) == -asech(3) + sqrt(2)*x/12 - \
    17*sqrt(2)*I*x**2/576 - 443*sqrt(2)*x**3/41472 + O(x**4)
    assert asech(-I*x + 3)._eval_nseries(x, 4, None) == asech(3) + sqrt(2)*x/12 + \
    17*sqrt(2)*I*x**2/576 - 443*sqrt(2)*x**3/41472 + O(x**4)
    assert asech(I*x - 3)._eval_nseries(x, 4, None) == -asech(-3) - sqrt(2)*x/12 - \
    17*sqrt(2)*I*x**2/576 + 443*sqrt(2)*x**3/41472 + O(x**4)
    assert asech(-I*x - 3)._eval_nseries(x, 4, None) == asech(-3) - sqrt(2)*x/12 + \
    17*sqrt(2)*I*x**2/576 + 443*sqrt(2)*x**3/41472 + O(x**4)
    # Tests concerning im(ndir) == 0
    assert asech(-I*x**2 + x - 2)._eval_nseries(x, 3, None) == 2*I*pi/3 + \
    x*(-sqrt(3) + 3*I)/(6*sqrt(3) + 6*I) + x**2*(36 + sqrt(3)*(7 - 12*I) + 21*I)/(72*sqrt(3) - \
    72*I) + O(x**3)

