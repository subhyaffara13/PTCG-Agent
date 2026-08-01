
def test_acsch_nseries():
    x = Symbol('x')
    # Tests concerning branch points
    assert acsch(x + I)._eval_nseries(x, 4, None) == -I*pi/2 + \
    sqrt(2)*I*sqrt(x)*sqrt(-I) - 5*x**(S(3)/2)*(1 - I)/12 - \
    43*sqrt(2)*I*x**(S(5)/2)*sqrt(-I)/160 + 177*x**(S(7)/2)*(1 - I)/896 + O(x**4)
    assert acsch(x - I)._eval_nseries(x, 4, None) == I*pi/2 - \
    sqrt(2)*sqrt(I)*I*sqrt(x) - 5*x**(S(3)/2)*(1 + I)/12 + \
    43*sqrt(2)*sqrt(I)*I*x**(S(5)/2)/160 + 177*x**(S(7)/2)*(1 + I)/896 + O(x**4)
    # Tests concerning points lying on branch cuts
    assert acsch(x + I/2)._eval_nseries(x, 4, None, cdir=1) == -acsch(I/2) - \
    I*pi + 4*sqrt(3)*I*x/3 - 8*sqrt(3)*x**2/9 - 16*sqrt(3)*I*x**3/9 + O(x**4)
    assert acsch(x + I/2)._eval_nseries(x, 4, None, cdir=-1) == acsch(I/2) - \
    4*sqrt(3)*I*x/3 + 8*sqrt(3)*x**2/9 + 16*sqrt(3)*I*x**3/9 + O(x**4)
    assert acsch(x - I/2)._eval_nseries(x, 4, None, cdir=1) == -acsch(I/2) - \
    4*sqrt(3)*I*x/3 - 8*sqrt(3)*x**2/9 + 16*sqrt(3)*I*x**3/9 + O(x**4)
    assert acsch(x - I/2)._eval_nseries(x, 4, None, cdir=-1) == I*pi + \
    acsch(I/2) + 4*sqrt(3)*I*x/3 + 8*sqrt(3)*x**2/9 - 16*sqrt(3)*I*x**3/9 + O(x**4)
    # Tests concerning re(ndir) == 0
    assert acsch(I/2 + I*x - x**2)._eval_nseries(x, 4, None) == -I*pi/2 + \
    log(2 - sqrt(3)) + x*(12 - 8*sqrt(3))/(-6 + 3*sqrt(3)) + x**2*(-96 + \
    sqrt(3)*(56 - 84*I) + 144*I)/(-63 + 36*sqrt(3)) + x**3*(2688 - 2688*I + \
    sqrt(3)*(-1552 + 1552*I))/(-873 + 504*sqrt(3)) + O(x**4)

