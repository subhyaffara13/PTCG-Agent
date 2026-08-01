
def test_is_disjoint():
    assert Interval(0, 2).is_disjoint(Interval(1, 2)) == False
    assert Interval(0, 2).is_disjoint(Interval(3, 4)) == True


def test_is_disjoint():
    eq = x**3 + 5*x + 1
    ir = rootof(eq, 0)._get_interval()
    ii = rootof(eq, 1)._get_interval()
    assert ir.is_disjoint(ii)
    assert ii.is_disjoint(ir)

