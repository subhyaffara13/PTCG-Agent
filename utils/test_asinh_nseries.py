
def test_asinh_nseries():
    x = Symbol('x')
    # Tests concerning branch points
    assert asinh(x + I)._eval_nseries(x, 4, None) == I*pi/2 - \
    sqrt(2)*sqrt(I)*I*sqrt(x) + sqrt(2)*sqrt(I)*x**(S(3)/2)/12 + 3*sqrt(2)*sqrt(I)*I*x**(S(5)/2)/160 - \
    5*sqrt(2)*sqrt(I)*x**(S(7)/2)/896 + O(x**4)
    assert asinh(x - I)._eval_nseries(x, 4, None) == -I*pi/2 + \
    sqrt(2)*I*sqrt(x)*sqrt(-I) + sqrt(2)*x**(S(3)/2)*sqrt(-I)/12 - \
    3*sqrt(2)*I*x**(S(5)/2)*sqrt(-I)/160 - 5*sqrt(2)*x**(S(7)/2)*sqrt(-I)/896 + O(x**4)
    # Tests concerning points lying on branch cuts
    assert asinh(x + 2*I)._eval_nseries(x, 4, None, cdir=1) == I*asin(2) - \
    sqrt(3)*I*x/3 + sqrt(3)*x**2/9 + sqrt(3)*I*x**3/18 + O(x**4)
    assert asinh(x + 2*I)._eval_nseries(x, 4, None, cdir=-1) == I*pi - I*asin(2) + \
    sqrt(3)*I*x/3 - sqrt(3)*x**2/9 - sqrt(3)*I*x**3/18 + O(x**4)
    assert asinh(x - 2*I)._eval_nseries(x, 4, None, cdir=1) == I*asin(2) - I*pi + \
    sqrt(3)*I*x/3 + sqrt(3)*x**2/9 - sqrt(3)*I*x**3/18 + O(x**4)
    assert asinh(x - 2*I)._eval_nseries(x, 4, None, cdir=-1) == -I*asin(2) - \
    sqrt(3)*I*x/3 - sqrt(3)*x**2/9 + sqrt(3)*I*x**3/18 + O(x**4)
    # Tests concerning re(ndir) == 0
    assert asinh(2*I + I*x - x**2)._eval_nseries(x, 4, None) == I*pi/2 + log(2 - sqrt(3)) + \
    x*(-3 + 2*sqrt(3))/(-6 + 3*sqrt(3)) + x**2*(12 - 36*I + sqrt(3)*(-7 + 21*I))/(-63 + \
    36*sqrt(3)) + x**3*(-168 + sqrt(3)*(97 - 388*I) + 672*I)/(-1746 + 1008*sqrt(3)) + O(x**4)

