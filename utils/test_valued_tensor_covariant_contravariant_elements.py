
def test_valued_tensor_covariant_contravariant_elements():
    with warns_deprecated_sympy():
        (A, B, AB, BA, C, Lorentz, E, px, py, pz, LorentzD, mu0, mu1, mu2, ndm, n0, n1,
         n2, NA, NB, NC, minkowski, ba_matrix, ndm_matrix, i0, i1, i2, i3, i4) = _get_valued_base_test_variables()

        assert A(-i0)[0] == A(i0)[0]
        assert A(-i0)[1] == -A(i0)[1]

        assert AB(i0, i1)[1, 1] == -1
        assert AB(i0, -i1)[1, 1] == 1
        assert AB(-i0, -i1)[1, 1] == -1
        assert AB(-i0, i1)[1, 1] == 1

