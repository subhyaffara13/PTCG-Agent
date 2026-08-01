
def test_atanh_nseries():
    x = Symbol('x')
    # Tests concerning branch points
    assert atanh(x + 1)._eval_nseries(x, 4, None, cdir=1) == -I*pi/2 + log(2)/2 - \
    log(x)/2 + x/4 - x**2/16 + x**3/48 + O(x**4)
    assert atanh(x + 1)._eval_nseries(x, 4, None, cdir=-1) == I*pi/2 + log(2)/2 - \
    log(x)/2 + x/4 - x**2/16 + x**3/48 + O(x**4)
    assert atanh(x - 1)._eval_nseries(x, 4, None, cdir=1) == -log(2)/2 + log(x)/2 + \
    x/4 + x**2/16 + x**3/48 + O(x**4)
    assert atanh(x - 1)._eval_nseries(x, 4, None, cdir=-1) == -log(2)/2 + log(x)/2 + \
    x/4 + x**2/16 + x**3/48 + O(x**4)
    # Tests concerning points lying on branch cuts
    assert atanh(I*x + 2)._eval_nseries(x, 4, None, cdir=1) == I*pi + atanh(2) - \
    I*x/3 - 2*x**2/9 + 13*I*x**3/81 + O(x**4)
    assert atanh(I*x + 2)._eval_nseries(x, 4, None, cdir=-1) == atanh(2) - I*x/3 - \
    2*x**2/9 + 13*I*x**3/81 + O(x**4)
    assert atanh(I*x - 2)._eval_nseries(x, 4, None, cdir=1) == -atanh(2) - I*x/3 + \
    2*x**2/9 + 13*I*x**3/81 + O(x**4)
    assert atanh(I*x - 2)._eval_nseries(x, 4, None, cdir=-1) == -atanh(2) - I*pi - \
    I*x/3 + 2*x**2/9 + 13*I*x**3/81 + O(x**4)
    # Tests concerning im(ndir) == 0
    assert atanh(-I*x**2 + x - 2)._eval_nseries(x, 4, None) == -I*pi/2 - log(3)/2 - x/3 + \
    x**2*(-S(1)/4 + I/2) + x**2*(S(1)/36 - I/6) + x**3*(-S(1)/6 + I/2) + x**3*(S(1)/162 - I/18) + O(x**4)

