
def test_evalf_divergent_series():
    raises(ValueError, lambda: Sum(1/n, (n, 1, oo)).evalf())
    raises(ValueError, lambda: Sum(n/(n**2 + 1), (n, 1, oo)).evalf())
    raises(ValueError, lambda: Sum((-1)**n, (n, 1, oo)).evalf())
    raises(ValueError, lambda: Sum((-1)**n, (n, 1, oo)).evalf())
    raises(ValueError, lambda: Sum(n**2, (n, 1, oo)).evalf())
    raises(ValueError, lambda: Sum(2**n, (n, 1, oo)).evalf())
    raises(ValueError, lambda: Sum((-2)**n, (n, 1, oo)).evalf())
    raises(ValueError, lambda: Sum((2*n + 3)/(3*n**2 + 4), (n, 0, oo)).evalf())
    raises(ValueError, lambda: Sum((0.5*n**3)/(n**4 + 1), (n, 0, oo)).evalf())

