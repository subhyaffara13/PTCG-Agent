
def test_schreier_vector():
    G = CyclicGroup(50)
    v = [0]*50
    v[23] = -1
    assert G.schreier_vector(23) == v
    H = DihedralGroup(8)
    assert H.schreier_vector(2) == [0, 1, -1, 0, 0, 1, 0, 0]
    L = SymmetricGroup(4)
    assert L.schreier_vector(1) == [1, -1, 0, 0]

