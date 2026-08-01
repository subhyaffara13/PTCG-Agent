
def test_Matrix_rep_domain():

    for Mat in MATRIX_TYPES:

        M = Mat([[1, 2], [3, 4]])
        assert M._rep == DMs([[1, 2], [3, 4]], ZZ)
        assert (M / 2)._rep == DMs([[(1,2), 1], [(3,2), 2]], QQ)
        if not isinstance(M, IMMUTABLE):
            M[0, 0] = x
            assert M._rep == DMs([[x, 2], [3, 4]], EXRAW)

        M = Mat([[S(1)/2, 2], [3, 4]])
        assert M._rep == DMs([[(1,2), 2], [3, 4]], QQ)
        if not isinstance(M, IMMUTABLE):
            M[0, 0] = x
            assert M._rep == DMs([[x, 2], [3, 4]], EXRAW)

        dM = DMs([[1, 2], [3, 4]], ZZ)
        assert Mat._fromrep(dM)._rep == dM

    # XXX: This is not intended. Perhaps it should be coerced to EXRAW?
    # The private _fromrep method is never called like this but perhaps it
    # should be guarded.
    #
    # It is not clear how to integrate domains other than ZZ, QQ and EXRAW with
    # the rest of Matrix or if the public type for this needs to be something
    # different from Matrix somehow.
    K = QQ.algebraic_field(sqrt(2))
    dM = DM([[1, 2], [3, 4]], K)
    assert Mat._fromrep(dM)._rep.domain == K

