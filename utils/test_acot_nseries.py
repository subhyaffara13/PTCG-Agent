
def test_acot_nseries():
    assert acot(x + S(1)/2*I)._eval_nseries(x, 4, None, 1) == -I*acoth(S(1)/2) + \
    pi - 4*x/3 + 8*I*x**2/9 + 112*x**3/81 + O(x**4)
    assert acot(x + S(1)/2*I)._eval_nseries(x, 4, None, -1) == -I*acoth(S(1)/2) - \
    4*x/3 + 8*I*x**2/9 + 112*x**3/81 + O(x**4)
    assert acot(x - S(1)/2*I)._eval_nseries(x, 4, None, 1) == I*acoth(S(1)/2) - \
    4*x/3 - 8*I*x**2/9 + 112*x**3/81 + O(x**4)
    assert acot(x - S(1)/2*I)._eval_nseries(x, 4, None, -1) == I*acoth(S(1)/2) - \
    pi - 4*x/3 - 8*I*x**2/9 + 112*x**3/81 + O(x**4)
    assert acot(x)._eval_nseries(x, 2, None, 1) == pi/2 - x + O(x**2)
    assert acot(x)._eval_nseries(x, 2, None, -1) == -pi/2 - x + O(x**2)
    # testing nseries for acot at branch points
    assert acot(x + I)._eval_nseries(x, 4, None) == -I*log(2)/2 + pi/4 + \
    I*log(x)/2 - x/4 - I*x**2/16 + x**3/48 + O(x**4)
    assert acot(x - I)._eval_nseries(x, 4, None) == I*log(2)/2 + pi/4 - \
    I*log(x)/2 - x/4 + I*x**2/16 + x**3/48 + O(x**4)

