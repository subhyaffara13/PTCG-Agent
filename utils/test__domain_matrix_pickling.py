
def test_DomainMatrix_pickling():
    import pickle
    dM = DomainMatrix({2: {2: ZZ(1)}, 4: {4: ZZ(1)}}, (5, 5), ZZ)
    assert pickle.loads(pickle.dumps(dM)) == dM
    dM = DomainMatrix([[ZZ(1), ZZ(2)], [ZZ(3), ZZ(4)]], (2, 2), ZZ)
    assert pickle.loads(pickle.dumps(dM)) == dM

