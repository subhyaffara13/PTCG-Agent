
def test_not_equal(a, b):
    assert a != b


def test_not_equal(Poly):
    p1 = Poly([1, 2, 3], domain=[0, 1], window=[2, 3])
    p2 = Poly([1, 1, 1], domain=[0, 1], window=[2, 3])
    p3 = Poly([1, 2, 3], domain=[1, 2], window=[2, 3])
    p4 = Poly([1, 2, 3], domain=[0, 1], window=[1, 2])
    assert_(not p1 != p1)
    assert_(p1 != p2)
    assert_(p1 != p3)
    assert_(p1 != p4)

