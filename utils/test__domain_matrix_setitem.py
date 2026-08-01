
def test_DomainMatrix_setitem():
    dM = DomainMatrix({2: {2: ZZ(1)}, 4: {4: ZZ(1)}}, (5, 5), ZZ)
    dM[2, 2] = ZZ(2)
    assert dM == DomainMatrix({2: {2: ZZ(2)}, 4: {4: ZZ(1)}}, (5, 5), ZZ)
    def setitem(i, j, val):
        dM[i, j] = val
    raises(TypeError, lambda: setitem(2, 2, QQ(1, 2)))
    raises(NotImplementedError, lambda: setitem(slice(1, 2), 2, ZZ(1)))

