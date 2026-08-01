
def test_log_nseries():
    p = Symbol('p')
    assert log(1/x)._eval_nseries(x, 4, logx=-p, cdir=1) == p
    assert log(1/x)._eval_nseries(x, 4, logx=-p, cdir=-1) == p + 2*I*pi
    assert log(x - 1)._eval_nseries(x, 4, None, I) == I*pi - x - x**2/2 - x**3/3 + O(x**4)
    assert log(x - 1)._eval_nseries(x, 4, None, -I) == -I*pi - x - x**2/2 - x**3/3 + O(x**4)
    assert log(I*x + I*x**3 - 1)._eval_nseries(x, 3, None, 1) == I*pi - I*x + x**2/2 + O(x**3)
    assert log(I*x + I*x**3 - 1)._eval_nseries(x, 3, None, -1) == -I*pi - I*x + x**2/2 + O(x**3)
    assert log(I*x**2 + I*x**3 - 1)._eval_nseries(x, 3, None, 1) == I*pi - I*x**2 + O(x**3)
    assert log(I*x**2 + I*x**3 - 1)._eval_nseries(x, 3, None, -1) == I*pi - I*x**2 + O(x**3)
    assert log(2*x + (3 - I)*x**2)._eval_nseries(x, 3, None, 1) == log(2) + log(x) + \
    x*(S(3)/2 - I/2) + x**2*(-1 + 3*I/4) + O(x**3)
    assert log(2*x + (3 - I)*x**2)._eval_nseries(x, 3, None, -1) == -2*I*pi + log(2) + \
    log(x) - x*(-S(3)/2 + I/2) + x**2*(-1 + 3*I/4) + O(x**3)
    assert log(-2*x + (3 - I)*x**2)._eval_nseries(x, 3, None, 1) == -I*pi + log(2) + log(x) + \
    x*(-S(3)/2 + I/2) + x**2*(-1 + 3*I/4) + O(x**3)
    assert log(-2*x + (3 - I)*x**2)._eval_nseries(x, 3, None, -1) == -I*pi + log(2) + log(x) - \
    x*(S(3)/2 - I/2) + x**2*(-1 + 3*I/4) + O(x**3)
    assert log(sqrt(-I*x**2 - 3)*sqrt(-I*x**2 - 1) - 2)._eval_nseries(x, 3, None, 1) == -I*pi + \
    log(sqrt(3) + 2) + 2*sqrt(3)*I*x**2/(3*sqrt(3) + 6) + O(x**3)
    assert log(-1/(1 - x))._eval_nseries(x, 3, None, 1) == I*pi + x + x**2/2 + O(x**3)
    assert log(-1/(1 - x))._eval_nseries(x, 3, None, -1) == I*pi + x + x**2/2 + O(x**3)

