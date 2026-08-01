
def test_asec_nseries():
    assert asec(x + S(1)/2)._eval_nseries(x, 4, None, I) == asec(S(1)/2) - \
    4*sqrt(3)*I*x/3 + 8*sqrt(3)*I*x**2/9 - 16*sqrt(3)*I*x**3/9 + O(x**4)
    assert asec(x + S(1)/2)._eval_nseries(x, 4, None, -I) == -asec(S(1)/2) + \
    4*sqrt(3)*I*x/3 - 8*sqrt(3)*I*x**2/9 + 16*sqrt(3)*I*x**3/9 + O(x**4)
    assert asec(x - S(1)/2)._eval_nseries(x, 4, None, I) == -asec(-S(1)/2) + \
    2*pi + 4*sqrt(3)*I*x/3 + 8*sqrt(3)*I*x**2/9 + 16*sqrt(3)*I*x**3/9 + O(x**4)
    assert asec(x - S(1)/2)._eval_nseries(x, 4, None, -I) == asec(-S(1)/2) - \
    4*sqrt(3)*I*x/3 - 8*sqrt(3)*I*x**2/9 - 16*sqrt(3)*I*x**3/9 + O(x**4)
    # testing nseries for asec at branch points
    assert asec(1 + x)._eval_nseries(x, 3, None) == sqrt(2)*sqrt(x) - \
    5*sqrt(2)*x**(S(3)/2)/12 + 43*sqrt(2)*x**(S(5)/2)/160 + O(x**3)
    assert asec(-1 + x)._eval_nseries(x, 3, None) == pi - sqrt(2)*sqrt(-x) + \
    5*sqrt(2)*(-x)**(S(3)/2)/12 - 43*sqrt(2)*(-x)**(S(5)/2)/160 + O(x**3)
    assert asec(exp(x))._eval_nseries(x, 3, None) == sqrt(2)*sqrt(x) - \
    sqrt(2)*x**(S(3)/2)/6 + sqrt(2)*x**(S(5)/2)/120 + O(x**3)
    assert asec(-exp(x))._eval_nseries(x, 3, None) == pi - sqrt(2)*sqrt(x) + \
    sqrt(2)*x**(S(3)/2)/6 - sqrt(2)*x**(S(5)/2)/120 + O(x**3)

