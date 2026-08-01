
def test_acoth_nseries():
    x = Symbol('x')
    # Tests concerning branch points
    assert acoth(x + 1)._eval_nseries(x, 4, None) == log(2)/2 - log(x)/2 + x/4 - \
    x**2/16 + x**3/48 + O(x**4)
    assert acoth(x - 1)._eval_nseries(x, 4, None, cdir=1) == I*pi/2 - log(2)/2 + \
    log(x)/2 + x/4 + x**2/16 + x**3/48 + O(x**4)
    assert acoth(x - 1)._eval_nseries(x, 4, None, cdir=-1) == -I*pi/2 - log(2)/2 + \
    log(x)/2 + x/4 + x**2/16 + x**3/48 + O(x**4)
    # Tests concerning points lying on branch cuts
    assert acoth(I*x + S(1)/2)._eval_nseries(x, 4, None, cdir=1) == acoth(S(1)/2) + \
    4*I*x/3 - 8*x**2/9 - 112*I*x**3/81 + O(x**4)
    assert acoth(I*x + S(1)/2)._eval_nseries(x, 4, None, cdir=-1) == I*pi + \
    acoth(S(1)/2) + 4*I*x/3 - 8*x**2/9 - 112*I*x**3/81 + O(x**4)
    assert acoth(I*x - S(1)/2)._eval_nseries(x, 4, None, cdir=1) == -acoth(S(1)/2) - \
    I*pi + 4*I*x/3 + 8*x**2/9 - 112*I*x**3/81 + O(x**4)
    assert acoth(I*x - S(1)/2)._eval_nseries(x, 4, None, cdir=-1) == -acoth(S(1)/2) + \
    4*I*x/3 + 8*x**2/9 - 112*I*x**3/81 + O(x**4)
    # Tests concerning im(ndir) == 0
    assert acoth(-I*x**2 - x - S(1)/2)._eval_nseries(x, 4, None) == I*pi/2 - log(3)/2 - \
    4*x/3 + x**2*(-S(8)/9 + 2*I/3) - 2*I*x**2 + x**3*(S(104)/81 - 16*I/9) - 8*x**3/3 + O(x**4)

