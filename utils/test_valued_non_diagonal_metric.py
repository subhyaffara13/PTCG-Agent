
def test_valued_non_diagonal_metric():
    with warns_deprecated_sympy():
        (A, B, AB, BA, C, Lorentz, E, px, py, pz, LorentzD, mu0, mu1, mu2, ndm, n0, n1,
         n2, NA, NB, NC, minkowski, ba_matrix, ndm_matrix, i0, i1, i2, i3, i4) = _get_valued_base_test_variables()

        mmatrix = Matrix(ndm_matrix)
        assert (NA(n0)*NA(-n0)).data == (NA(n0).get_matrix().T * mmatrix * NA(n0).get_matrix())[0, 0]

