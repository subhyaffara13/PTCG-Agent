
def test_exp_product_positive_factors():
    a, b = symbols('a, b', positive=True)
    x = a * b
    assert series(exp(x), x, n=8) == 1 + a*b + a**2*b**2/2 + \
        a**3*b**3/6 + a**4*b**4/24 + a**5*b**5/120 + a**6*b**6/720 + \
        a**7*b**7/5040 + O(a**8*b**8, a, b)

