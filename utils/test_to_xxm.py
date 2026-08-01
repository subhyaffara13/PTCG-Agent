
def test_to_XXM():
    """Test to_ddm etc. for DDM, SDM, DFM and DomainMatrix."""

    lol = [[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]]
    dod = {0: {0: ZZ(1), 1: ZZ(2)}, 1: {0: ZZ(3), 1: ZZ(4)}}

    A_ddm = DDM(lol, (2, 2), ZZ)
    A_sdm = SDM(dod, (2, 2), ZZ)
    A_dm_d = DomainMatrix(lol, (2, 2), ZZ)
    A_dm_s = DomainMatrix(dod, (2, 2), ZZ)

    A_all = [A_ddm, A_sdm, A_dm_d, A_dm_s]

    if GROUND_TYPES == 'flint':
        A_dfm = DFM(lol, (2, 2), ZZ)
        A_all.append(A_dfm)

    for A in A_all:
        assert A.to_ddm() == A_ddm
        assert A.to_sdm() == A_sdm
        if GROUND_TYPES != 'flint':
            raises(NotImplementedError, lambda: A.to_dfm())
            assert A.to_dfm_or_ddm() == A_ddm

        # Add e.g. DDM.to_DM()?
        # assert A.to_DM() == A_dm

    if GROUND_TYPES == 'flint':
        for A in A_all:
            assert A.to_dfm() == A_dfm
            for K in [ZZ, QQ, GF(5), ZZ_I]:
                if isinstance(A, DFM) and not DFM._supports_domain(K):
                    raises(NotImplementedError, lambda: A.convert_to(K))
                else:
                    A_K = A.convert_to(K)
                    if DFM._supports_domain(K):
                        A_dfm_K = A_dfm.convert_to(K)
                        assert A_K.to_dfm() == A_dfm_K
                        assert A_K.to_dfm_or_ddm() == A_dfm_K
                    else:
                        raises(NotImplementedError, lambda: A_K.to_dfm())
                        assert A_K.to_dfm_or_ddm() == A_ddm.convert_to(K)

