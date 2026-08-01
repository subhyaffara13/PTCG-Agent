
def test_XXM_constructors():
    """Test the DDM, etc constructors."""

    lol = [
        [ZZ(1), ZZ(2)],
        [ZZ(3), ZZ(4)],
        [ZZ(5), ZZ(6)],
    ]
    dod = {
        0: {0: ZZ(1), 1: ZZ(2)},
        1: {0: ZZ(3), 1: ZZ(4)},
        2: {0: ZZ(5), 1: ZZ(6)},
    }

    lol_0x0 = []
    lol_0x2 = []
    lol_2x0 = [[], []]
    dod_0x0 = {}
    dod_0x2 = {}
    dod_2x0 = {}

    lol_bad = [
        [ZZ(1), ZZ(2)],
        [ZZ(3), ZZ(4)],
        [ZZ(5), ZZ(6), ZZ(7)],
    ]
    dod_bad = {
        0: {0: ZZ(1), 1: ZZ(2)},
        1: {0: ZZ(3), 1: ZZ(4)},
        2: {0: ZZ(5), 1: ZZ(6), 2: ZZ(7)},
    }

    XDM_dense = [DDM]
    XDM_sparse = [SDM]

    if GROUND_TYPES == 'flint':
        XDM_dense.append(DFM)

    for XDM in XDM_dense:

        A = XDM(lol, (3, 2), ZZ)
        assert A.rows == 3
        assert A.cols == 2
        assert A.domain == ZZ
        assert A.shape == (3, 2)
        if XDM is not DFM:
            assert ZZ.of_type(A[0][0]) is True
        else:
            assert ZZ.of_type(A.rep[0, 0]) is True

        Adm = DomainMatrix(lol, (3, 2), ZZ)
        if XDM is DFM:
            assert Adm.rep == A
            assert Adm.rep.to_ddm() != A
        elif GROUND_TYPES == 'flint':
            assert Adm.rep.to_ddm() == A
            assert Adm.rep != A
        else:
            assert Adm.rep == A
            assert Adm.rep.to_ddm() == A

        assert XDM(lol_0x0, (0, 0), ZZ).shape == (0, 0)
        assert XDM(lol_0x2, (0, 2), ZZ).shape == (0, 2)
        assert XDM(lol_2x0, (2, 0), ZZ).shape == (2, 0)
        raises(DMBadInputError, lambda: XDM(lol, (2, 3), ZZ))
        raises(DMBadInputError, lambda: XDM(lol_bad, (3, 2), ZZ))
        raises(DMBadInputError, lambda: XDM(dod, (3, 2), ZZ))

    for XDM in XDM_sparse:

        A = XDM(dod, (3, 2), ZZ)
        assert A.rows == 3
        assert A.cols == 2
        assert A.domain == ZZ
        assert A.shape == (3, 2)
        assert ZZ.of_type(A[0][0]) is True

        assert DomainMatrix(dod, (3, 2), ZZ).rep == A

        assert XDM(dod_0x0, (0, 0), ZZ).shape == (0, 0)
        assert XDM(dod_0x2, (0, 2), ZZ).shape == (0, 2)
        assert XDM(dod_2x0, (2, 0), ZZ).shape == (2, 0)
        raises(DMBadInputError, lambda: XDM(dod, (2, 3), ZZ))
        raises(DMBadInputError, lambda: XDM(lol, (3, 2), ZZ))
        raises(DMBadInputError, lambda: XDM(dod_bad, (3, 2), ZZ))

    raises(DMBadInputError, lambda: DomainMatrix(lol, (2, 3), ZZ))
    raises(DMBadInputError, lambda: DomainMatrix(lol_bad, (3, 2), ZZ))
    raises(DMBadInputError, lambda: DomainMatrix(dod_bad, (3, 2), ZZ))

