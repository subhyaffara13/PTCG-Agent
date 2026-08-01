
def test_PrimeIdeal_eq():
    # `==` should fail on objects of different types, so even a completely
    # inert PrimeIdeal should test unequal to the rational prime it divides.
    T = Poly(cyclotomic_poly(7))
    P0 = prime_decomp(5, T)[0]
    assert P0.f == 6
    assert P0.as_submodule() == 5 * P0.ZK
    assert P0 != 5

