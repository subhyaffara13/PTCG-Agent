
def test_valued_tensor_add_scalar():
    with warns_deprecated_sympy():
        (A, B, AB, BA, C, Lorentz, E, px, py, pz, LorentzD, mu0, mu1, mu2, ndm, n0, n1,
         n2, NA, NB, NC, minkowski, ba_matrix, ndm_matrix, i0, i1, i2, i3, i4) = _get_valued_base_test_variables()

        # one scalar summand after the contracted tensor
        expr1 = A(i0)*A(-i0) - (E**2 - px**2 - py**2 - pz**2)
        assert expr1.data == 0

        # multiple scalar summands in front of the contracted tensor
        expr2 = E**2 - px**2 - py**2 - pz**2 - A(i0)*A(-i0)
        assert expr2.data == 0

        # multiple scalar summands after the contracted tensor
        expr3 =  A(i0)*A(-i0) - E**2 + px**2 + py**2 + pz**2
        assert expr3.data == 0

        # multiple scalar summands and multiple tensors
        expr4 = C(mu0)*C(-mu0) + 2*E**2 - 2*px**2 - 2*py**2 - 2*pz**2 - A(i0)*A(-i0)
        assert expr4.data == 0

