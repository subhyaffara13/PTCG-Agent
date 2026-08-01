
def test_acsc_nseries():
    assert acsc(x + S(1)/2)._eval_nseries(x, 4, None, I) == acsc(S(1)/2) + \
    4*sqrt(3)*I*x/3 - 8*sqrt(3)*I*x**2/9 + 16*sqrt(3)*I*x**3/9 + O(x**4)
    assert acsc(x + S(1)/2)._eval_nseries(x, 4, None, -I) == -acsc(S(1)/2) + \
    pi - 4*sqrt(3)*I*x/3 + 8*sqrt(3)*I*x**2/9 - 16*sqrt(3)*I*x**3/9 + O(x**4)
    assert acsc(x - S(1)/2)._eval_nseries(x, 4, None, I) == acsc(S(1)/2) - pi -\
    4*sqrt(3)*I*x/3 - 8*sqrt(3)*I*x**2/9 - 16*sqrt(3)*I*x**3/9 + O(x**4)
    assert acsc(x - S(1)/2)._eval_nseries(x, 4, None, -I) == -acsc(S(1)/2) + \
    4*sqrt(3)*I*x/3 + 8*sqrt(3)*I*x**2/9 + 16*sqrt(3)*I*x**3/9 + O(x**4)
    # testing nseries for acsc at branch points
    assert acsc(1 + x)._eval_nseries(x, 3, None) == pi/2 - sqrt(2)*sqrt(x) + \
    5*sqrt(2)*x**(S(3)/2)/12 - 43*sqrt(2)*x**(S(5)/2)/160 + O(x**3)
    assert acsc(-1 + x)._eval_nseries(x, 3, None) == -pi/2 + sqrt(2)*sqrt(-x) - \
    5*sqrt(2)*(-x)**(S(3)/2)/12 + 43*sqrt(2)*(-x)**(S(5)/2)/160 + O(x**3)
    assert acsc(exp(x))._eval_nseries(x, 3, None) == pi/2 - sqrt(2)*sqrt(x) + \
    sqrt(2)*x**(S(3)/2)/6 - sqrt(2)*x**(S(5)/2)/120 + O(x**3)
    assert acsc(-exp(x))._eval_nseries(x, 3, None) == -pi/2 + sqrt(2)*sqrt(x) - \
    sqrt(2)*x**(S(3)/2)/6 + sqrt(2)*x**(S(5)/2)/120 + O(x**3)

