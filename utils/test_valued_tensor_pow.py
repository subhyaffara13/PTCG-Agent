
def test_valued_tensor_pow():
    with warns_deprecated_sympy():
        (A, B, AB, BA, C, Lorentz, E, px, py, pz, LorentzD, mu0, mu1, mu2, ndm, n0, n1,
         n2, NA, NB, NC, minkowski, ba_matrix, ndm_matrix, i0, i1, i2, i3, i4) = _get_valued_base_test_variables()

        assert C**2 == -E**2 + px**2 + py**2 + pz**2
        assert C**1 == sqrt(-E**2 + px**2 + py**2 + pz**2)
        assert C(mu0)**2 == C**2
        assert C(mu0)**1 == C**1

