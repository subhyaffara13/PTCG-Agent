
def test_valued_tensor_get_matrix():
    with warns_deprecated_sympy():
        (A, B, AB, BA, C, Lorentz, E, px, py, pz, LorentzD, mu0, mu1, mu2, ndm, n0, n1,
         n2, NA, NB, NC, minkowski, ba_matrix, ndm_matrix, i0, i1, i2, i3, i4) = _get_valued_base_test_variables()

        matab = AB(i0, i1).get_matrix()
        assert matab == Matrix([
                                [1,  0,  0,  0],
                                [0, -1,  0,  0],
                                [0,  0, -1,  0],
                                [0,  0,  0, -1],
                                ])
        # when alternating contravariant/covariant with [1, -1, -1, -1] metric
        # it becomes the identity matrix:
        assert AB(i0, -i1).get_matrix() == eye(4)

        # covariant and contravariant forms:
        assert A(i0).get_matrix() == Matrix([E, px, py, pz])
        assert A(-i0).get_matrix() == Matrix([E, -px, -py, -pz])

