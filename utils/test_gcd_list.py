
def test_gcd_list():
    F = [x**3 - 1, x**2 - 1, x**2 - 3*x + 2]

    assert gcd_list(F) == x - 1
    assert gcd_list(F, polys=True) == Poly(x - 1)

    assert gcd_list([]) == 0
    assert gcd_list([1, 2]) == 1
    assert gcd_list([4, 6, 8]) == 2

    assert gcd_list([x*(y + 42) - x*y - x*42]) == 0

    gcd = gcd_list([], x)
    assert gcd.is_Number and gcd is S.Zero

    gcd = gcd_list([], x, polys=True)
    assert gcd.is_Poly and gcd.is_zero

    a = sqrt(2)
    assert gcd_list([a, -a]) == gcd_list([-a, a]) == a

    raises(ComputationFailed, lambda: gcd_list([], polys=True))

