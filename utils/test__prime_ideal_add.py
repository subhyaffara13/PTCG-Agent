
def test_PrimeIdeal_add():
    T = Poly(cyclotomic_poly(7))
    P0 = prime_decomp(7, T)[0]
    # Adding ideals computes their GCD, so adding the ramified prime dividing
    # 7 to 7 itself should reproduce this prime (as a submodule).
    assert P0 + 7 * P0.ZK == P0.as_submodule()

