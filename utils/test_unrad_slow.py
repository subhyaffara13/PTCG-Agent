
def test_unrad_slow():
    # this has roots with multiplicity > 1; there should be no
    # repeats in roots obtained, however
    eq = (sqrt(1 + sqrt(1 - 4*x**2)) - x*(1 + sqrt(1 + 2*sqrt(1 - 4*x**2))))
    assert solve(eq) == [S.Half]

