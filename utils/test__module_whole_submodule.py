
def test_Module_whole_submodule():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    B = A.whole_submodule()
    e = B(to_col([1, 2, 3, 4]))
    f = e.to_parent()
    assert f.col.flat() == [1, 2, 3, 4]
    e0, e1, e2, e3 = B(0), B(1), B(2), B(3)
    assert e2 * e3 == e0
    assert e3 ** 2 == e1

