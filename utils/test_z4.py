
def test_Z4():
# => [c^(n+1) [c^(n+1) - 2 c - 2] + (n+1) c^2 + 2 c - n] / [(c-1)^3 (c+1)]
#    [Joan Z. Yu and Robert Israel in sci.math.symbolic]
    r = Function('r')
    c = symbols('c')
    # raises ValueError: Polynomial or rational function expected,
    #     got '(c**2 - c**n)/(c - c**n)
    s = rsolve(r(n) - ((1 + c - c**(n-1) - c**(n+1))/(1 - c**n)*r(n - 1)
                   - c*(1 - c**(n-2))/(1 - c**(n-1))*r(n - 2) + 1),
           r(n), {r(1): 1, r(2): (2 + 2*c + c**2)/(1 + c)})
    assert (s - (c*(n + 1)*(c*(n + 1) - 2*c - 2) +
             (n + 1)*c**2 + 2*c - n)/((c-1)**3*(c+1)) == 0)

