
def test_lcm_list():
    F = [x**3 - 1, x**2 - 1, x**2 - 3*x + 2]

    assert lcm_list(F) == x**5 - x**4 - 2*x**3 - x**2 + x + 2
    assert lcm_list(F, polys=True) == Poly(x**5 - x**4 - 2*x**3 - x**2 + x + 2)

    assert lcm_list([]) == 1
    assert lcm_list([1, 2]) == 2
    assert lcm_list([4, 6, 8]) == 24

    assert lcm_list([x*(y + 42) - x*y - x*42]) == 0

    lcm = lcm_list([], x)
    assert lcm.is_Number and lcm is S.One

    lcm = lcm_list([], x, polys=True)
    assert lcm.is_Poly and lcm.is_one

    raises(ComputationFailed, lambda: lcm_list([], polys=True))

