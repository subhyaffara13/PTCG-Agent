
def test_ternary_quadratic():
    # solution with 3 parameters
    s = diophantine(2*x**2 + y**2 - 2*z**2)
    p, q, r = ordered(S(s).free_symbols)
    assert s == {(
        p**2 - 2*q**2,
        -2*p**2 + 4*p*q - 4*p*r - 4*q**2,
        p**2 - 4*p*q + 2*q**2 - 4*q*r)}
    # solution with Mul in solution
    s = diophantine(x**2 + 2*y**2 - 2*z**2)
    assert s == {(4*p*q, p**2 - 2*q**2, p**2 + 2*q**2)}
    # solution with no Mul in solution
    s = diophantine(2*x**2 + 2*y**2 - z**2)
    assert s == {(2*p**2 - q**2, -2*p**2 + 4*p*q - q**2,
        4*p**2 - 4*p*q + 2*q**2)}
    # reduced form when parametrized
    s = diophantine(3*x**2 + 72*y**2 - 27*z**2)
    assert s == {(24*p**2 - 9*q**2, 6*p*q, 8*p**2 + 3*q**2)}
    assert parametrize_ternary_quadratic(
        3*x**2 + 2*y**2 - z**2 - 2*x*y + 5*y*z - 7*y*z) == (
        2*p**2 - 2*p*q - q**2, 2*p**2 + 2*p*q - q**2, 2*p**2 -
        2*p*q + 3*q**2)
    assert parametrize_ternary_quadratic(
        124*x**2 - 30*y**2 - 7729*z**2) == (
        -1410*p**2 - 363263*q**2, 2700*p**2 + 30916*p*q -
        695610*q**2, -60*p**2 + 5400*p*q + 15458*q**2)

