
def test_asin_nseries():
    assert asin(x + 2)._eval_nseries(x, 4, None, I) == -asin(2) + pi + \
    sqrt(3)*I*x/3 - sqrt(3)*I*x**2/9 + sqrt(3)*I*x**3/18 + O(x**4)
    assert asin(x + 2)._eval_nseries(x, 4, None, -I) == asin(2) - \
    sqrt(3)*I*x/3 + sqrt(3)*I*x**2/9 - sqrt(3)*I*x**3/18 + O(x**4)
    assert asin(x - 2)._eval_nseries(x, 4, None, I) == -asin(2) - \
    sqrt(3)*I*x/3 - sqrt(3)*I*x**2/9 - sqrt(3)*I*x**3/18 + O(x**4)
    assert asin(x - 2)._eval_nseries(x, 4, None, -I) == asin(2) - pi + \
    sqrt(3)*I*x/3 + sqrt(3)*I*x**2/9 + sqrt(3)*I*x**3/18 + O(x**4)
    # testing nseries for asin at branch points
    assert asin(1 + x)._eval_nseries(x, 3, None) == pi/2 - sqrt(2)*sqrt(-x) - \
    sqrt(2)*(-x)**(S(3)/2)/12 - 3*sqrt(2)*(-x)**(S(5)/2)/160 + O(x**3)
    assert asin(-1 + x)._eval_nseries(x, 3, None) == -pi/2 + sqrt(2)*sqrt(x) + \
    sqrt(2)*x**(S(3)/2)/12 + 3*sqrt(2)*x**(S(5)/2)/160 + O(x**3)
    assert asin(exp(x))._eval_nseries(x, 3, None) == pi/2 - sqrt(2)*sqrt(-x) + \
    sqrt(2)*(-x)**(S(3)/2)/6 - sqrt(2)*(-x)**(S(5)/2)/120 + O(x**3)
    assert asin(-exp(x))._eval_nseries(x, 3, None) == -pi/2 + sqrt(2)*sqrt(-x) - \
    sqrt(2)*(-x)**(S(3)/2)/6 + sqrt(2)*(-x)**(S(5)/2)/120 + O(x**3)

