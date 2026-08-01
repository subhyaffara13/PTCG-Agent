
def test_inverse_inexact():

    M = Matrix([[x-0.3, -0.06, -0.22],
                [-0.46, x-0.48, -0.41],
                [-0.14, -0.39, x-0.64]])

    Mn = Matrix([[1.0*x**2 - 1.12*x + 0.1473, 0.06*x + 0.0474, 0.22*x - 0.081],
                 [0.46*x - 0.237, 1.0*x**2 - 0.94*x + 0.1612, 0.41*x - 0.0218],
                 [0.14*x + 0.1122, 0.39*x - 0.1086, 1.0*x**2 - 0.78*x + 0.1164]])

    d = 1.0*x**3 - 1.42*x**2 + 0.4249*x - 0.0546540000000002

    Mi = Mn / d

    M_dm = M.to_DM()
    M_dmd = M_dm.to_dense()
    M_dm_num, M_dm_den = M_dm.inv_den()
    M_dmd_num, M_dmd_den = M_dmd.inv_den()

    # XXX: We don't check M_dm().to_field().inv() which currently uses division
    # and produces a more complicate result from gcd cancellation failing.
    # DomainMatrix.inv() over RR(x) should be changed to clear denominators and
    # use DomainMatrix.inv_den().

    Minvs = [
        M.inv(),
        (M_dm_num.to_field() / M_dm_den).to_Matrix(),
        (M_dmd_num.to_field() / M_dmd_den).to_Matrix(),
        M_dm_num.to_Matrix() / M_dm_den.as_expr(),
        M_dmd_num.to_Matrix() / M_dmd_den.as_expr(),
    ]

    for Minv in Minvs:
        for Mi1, Mi2 in zip(Minv.flat(), Mi.flat()):
            assert all_close(Mi2, Mi1)

