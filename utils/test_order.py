
def test_order():
    F, x, y = free_group("x, y")
    f = FpGroup(F, [x**4, y**2, x*y*x**-1*y])
    assert f.order() == 8

    f = FpGroup(F, [x*y*x**-1*y**-1, y**2])
    assert f.order() is S.Infinity

    F, a, b, c = free_group("a, b, c")
    f = FpGroup(F, [a**250, b**2, c*b*c**-1*b, c**4, c**-1*a**-1*c*a, a**-1*b**-1*a*b])
    assert f.order() == 2000

    F, x = free_group("x")
    f = FpGroup(F, [])
    assert f.order() is S.Infinity

    f = FpGroup(free_group('')[0], [])
    assert f.order() == 1


def test_order():
    a = Permutation([2, 0, 1, 3, 4, 5, 6, 7, 8, 9])
    b = Permutation([2, 1, 3, 4, 5, 6, 7, 8, 9, 0])
    g = PermutationGroup([a, b])
    assert g.order() == 1814400
    assert PermutationGroup().order() == 1

