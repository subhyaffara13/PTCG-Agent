
def test_atan_nseries():
    assert atan(x + 2*I)._eval_nseries(x, 4, None, 1) == I*atanh(2) - x/3 - \
    2*I*x**2/9 + 13*x**3/81 + O(x**4)
    assert atan(x + 2*I)._eval_nseries(x, 4, None, -1) == I*atanh(2) - pi - \
    x/3 - 2*I*x**2/9 + 13*x**3/81 + O(x**4)
    assert atan(x - 2*I)._eval_nseries(x, 4, None, 1) == -I*atanh(2) + pi - \
    x/3 + 2*I*x**2/9 + 13*x**3/81 + O(x**4)
    assert atan(x - 2*I)._eval_nseries(x, 4, None, -1) == -I*atanh(2) - x/3 + \
    2*I*x**2/9 + 13*x**3/81 + O(x**4)
    assert atan(1/x)._eval_nseries(x, 2, None, 1) == pi/2 - x + O(x**2)
    assert atan(1/x)._eval_nseries(x, 2, None, -1) == -pi/2 - x + O(x**2)
    # testing nseries for atan at branch points
    assert atan(x + I)._eval_nseries(x, 4, None) == I*log(2)/2 + pi/4 - \
    I*log(x)/2 + x/4 + I*x**2/16 - x**3/48 + O(x**4)
    assert atan(x - I)._eval_nseries(x, 4, None) == -I*log(2)/2 + pi/4 + \
    I*log(x)/2 + x/4 - I*x**2/16 - x**3/48 + O(x**4)

