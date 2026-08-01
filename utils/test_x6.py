
def test_X6():
    # Taylor series of nonscalar objects (noncommutative multiplication)
    # expected result => (B A - A B) t^2/2 + O(t^3)   [Stanly Steinberg]
    a, b = symbols('a b', commutative=False, scalar=False)
    assert (series(exp((a + b)*x) - exp(a*x) * exp(b*x), x, x0=0, n=3) ==
              x**2*(-a*b/2 + b*a/2) + O(x**3))

