
def test_concyclic_doctest_bug():
    p1, p2 = Point(-1, 0), Point(1, 0)
    p3, p4 = Point(0, 1), Point(-1, 2)
    assert Point.is_concyclic(p1, p2, p3)
    assert not Point.is_concyclic(p1, p2, p3, p4)

