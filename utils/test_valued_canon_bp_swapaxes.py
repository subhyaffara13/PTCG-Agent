
def test_valued_canon_bp_swapaxes():
    with warns_deprecated_sympy():
        (A, B, AB, BA, C, Lorentz, E, px, py, pz, LorentzD, mu0, mu1, mu2, ndm, n0, n1,
         n2, NA, NB, NC, minkowski, ba_matrix, ndm_matrix, i0, i1, i2, i3, i4) = _get_valued_base_test_variables()

        e1 = A(i1)*A(i0)
        e2 = e1.canon_bp()
        assert e2 == A(i0)*A(i1)
        for i in range(4):
            for j in range(4):
                assert e1[i, j] == e2[j, i]
        o1 = B(i2)*A(i1)*B(i0)
        o2 = o1.canon_bp()
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    assert o1[i, j, k] == o2[j, i, k]

