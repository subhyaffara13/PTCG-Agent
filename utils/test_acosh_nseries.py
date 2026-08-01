
def test_acosh_nseries():
    x = Symbol('x')
    # Tests concerning branch points
    assert acosh(x + 1)._eval_nseries(x, 4, None) == sqrt(2)*sqrt(x) - \
    sqrt(2)*x**(S(3)/2)/12 + 3*sqrt(2)*x**(S(5)/2)/160 - 5*sqrt(2)*x**(S(7)/2)/896 + O(x**4)
    # Tests concerning points lying on branch cuts
    assert acosh(x - 1)._eval_nseries(x, 4, None) == I*pi - \
    sqrt(2)*I*sqrt(x) - sqrt(2)*I*x**(S(3)/2)/12 - 3*sqrt(2)*I*x**(S(5)/2)/160 - \
    5*sqrt(2)*I*x**(S(7)/2)/896 + O(x**4)
    assert acosh(I*x - 2)._eval_nseries(x, 4, None, cdir=1) == acosh(-2) - \
    sqrt(3)*I*x/3 + sqrt(3)*x**2/9 + sqrt(3)*I*x**3/18 + O(x**4)
    assert acosh(-I*x - 2)._eval_nseries(x, 4, None, cdir=1) == acosh(-2) - \
    2*I*pi + sqrt(3)*I*x/3 + sqrt(3)*x**2/9 - sqrt(3)*I*x**3/18 + O(x**4)
    assert acosh(1/(I*x - 3))._eval_nseries(x, 4, None, cdir=1) == -acosh(-S(1)/3) + \
    sqrt(2)*x/12 + 17*sqrt(2)*I*x**2/576 - 443*sqrt(2)*x**3/41472 + O(x**4)
    assert acosh(1/(I*x - 3))._eval_nseries(x, 4, None, cdir=-1) == acosh(-S(1)/3) - \
    sqrt(2)*x/12 - 17*sqrt(2)*I*x**2/576 + 443*sqrt(2)*x**3/41472 + O(x**4)
    # Tests concerning im(ndir) == 0
    assert acosh(-I*x**2 + x - 2)._eval_nseries(x, 4, None) == -I*pi + log(sqrt(3) + 2) + \
    x*(-2*sqrt(3) - 3)/(3*sqrt(3) + 6) + x**2*(-12 + 36*I + sqrt(3)*(-7 + 21*I))/(36*sqrt(3) + \
    63) + x**3*(-168 + 672*I + sqrt(3)*(-97 + 388*I))/(1008*sqrt(3) + 1746) + O(x**4)

