
def test_DDM_applyfunc():
    A = DDM([[ZZ(1), ZZ(2), ZZ(3)]], (1, 3), ZZ)
    B = DDM([[ZZ(2), ZZ(4), ZZ(6)]], (1, 3), ZZ)
    assert A.applyfunc(lambda x: 2*x, ZZ) == B

