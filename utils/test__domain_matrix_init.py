
def test_DomainMatrix_init():
    lol = [[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]]
    dod = {0: {0: ZZ(1), 1:ZZ(2)}, 1: {0:ZZ(3), 1:ZZ(4)}}
    ddm = DDM(lol, (2, 2), ZZ)
    sdm = SDM(dod, (2, 2), ZZ)

    A = DomainMatrix(lol, (2, 2), ZZ)
    if GROUND_TYPES != 'flint':
        assert A.rep == ddm
    else:
        assert A.rep == ddm.to_dfm()
    assert A.shape == (2, 2)
    assert A.domain == ZZ

    A = DomainMatrix(dod, (2, 2), ZZ)
    assert A.rep == sdm
    assert A.shape == (2, 2)
    assert A.domain == ZZ

    raises(TypeError, lambda: DomainMatrix(ddm, (2, 2), ZZ))
    raises(TypeError, lambda: DomainMatrix(sdm, (2, 2), ZZ))
    raises(TypeError, lambda: DomainMatrix(Matrix([[1]]), (1, 1), ZZ))

    for fmt, rep in [('sparse', sdm), ('dense', ddm)]:
        if fmt == 'dense' and GROUND_TYPES == 'flint':
            rep = rep.to_dfm()
        A = DomainMatrix(lol, (2, 2), ZZ, fmt=fmt)
        assert A.rep == rep
        A = DomainMatrix(dod, (2, 2), ZZ, fmt=fmt)
        assert A.rep == rep

    raises(ValueError, lambda: DomainMatrix(lol, (2, 2), ZZ, fmt='invalid'))

    raises(DMBadInputError, lambda: DomainMatrix([[ZZ(1), ZZ(2)]], (2, 2), ZZ))

    # uses copy
    was = [i.copy() for i in lol]
    A[0,0] = ZZ(42)
    assert was == lol

