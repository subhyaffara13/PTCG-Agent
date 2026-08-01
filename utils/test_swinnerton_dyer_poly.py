
def test_swinnerton_dyer_poly():
    raises(ValueError, lambda: swinnerton_dyer_poly(0, x))

    assert swinnerton_dyer_poly(1, x, polys=True) == Poly(x**2 - 2)

    assert swinnerton_dyer_poly(1, x) == x**2 - 2
    assert swinnerton_dyer_poly(2, x) == x**4 - 10*x**2 + 1
    assert swinnerton_dyer_poly(
        3, x) == x**8 - 40*x**6 + 352*x**4 - 960*x**2 + 576
    # we only need to check that the polys arg works but
    # we may as well test that the roots are correct
    p = [sqrt(prime(i)) for i in range(1, 5)]
    assert str([i.n(3) for i in
        swinnerton_dyer_poly(4, polys=True).all_roots()]
        ) == str(sorted([Add(*i).n(3) for i in permute_signs(p)]))

