
def test_XXM_eq():
    """Test equality for DDM, SDM, DFM and DomainMatrix."""

    lol1 = [[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]]
    dod1 = {0: {0: ZZ(1), 1: ZZ(2)}, 1: {0: ZZ(3), 1: ZZ(4)}}

    lol2 = [[ZZ(1), ZZ(2)], [ZZ(3), ZZ(5)]]
    dod2 = {0: {0: ZZ(1), 1: ZZ(2)}, 1: {0: ZZ(3), 1: ZZ(5)}}

    A1_ddm = DDM(lol1, (2, 2), ZZ)
    A1_sdm = SDM(dod1, (2, 2), ZZ)
    A1_dm_d = DomainMatrix(lol1, (2, 2), ZZ)
    A1_dm_s = DomainMatrix(dod1, (2, 2), ZZ)

    A2_ddm = DDM(lol2, (2, 2), ZZ)
    A2_sdm = SDM(dod2, (2, 2), ZZ)
    A2_dm_d = DomainMatrix(lol2, (2, 2), ZZ)
    A2_dm_s = DomainMatrix(dod2, (2, 2), ZZ)

    A1_all = [A1_ddm, A1_sdm, A1_dm_d, A1_dm_s]
    A2_all = [A2_ddm, A2_sdm, A2_dm_d, A2_dm_s]

    if GROUND_TYPES == 'flint':

        A1_dfm = DFM([[1, 2], [3, 4]], (2, 2), ZZ)
        A2_dfm = DFM([[1, 2], [3, 5]], (2, 2), ZZ)

        A1_all.append(A1_dfm)
        A2_all.append(A2_dfm)

    for n, An in enumerate(A1_all):
        for m, Am in enumerate(A1_all):
            if n == m:
                assert (An == Am) is True
                assert (An != Am) is False
            else:
                assert (An == Am) is False
                assert (An != Am) is True

    for n, An in enumerate(A2_all):
        for m, Am in enumerate(A2_all):
            if n == m:
                assert (An == Am) is True
                assert (An != Am) is False
            else:
                assert (An == Am) is False
                assert (An != Am) is True

    for n, A1 in enumerate(A1_all):
        for m, A2 in enumerate(A2_all):
            assert (A1 == A2) is False
            assert (A1 != A2) is True

