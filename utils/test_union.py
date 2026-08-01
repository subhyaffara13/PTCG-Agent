
def test_union():
    instance = m.TestUnion()

    instance.as_uint = 10
    assert instance.as_int == 10


def test_union():
    N = Normal('N', 3, 2)
    assert simplify(P(N**2 - N > 2)) == \
        -erf(sqrt(2))/2 - erfc(sqrt(2)/4)/2 + Rational(3, 2)
    assert simplify(P(N**2 - 4 > 0)) == \
        -erf(5*sqrt(2)/4)/2 - erfc(sqrt(2)/4)/2 + Rational(3, 2)


def test_union():
    assert Union(Interval(1, 2), Interval(2, 3)) == Interval(1, 3)
    assert Union(Interval(1, 2), Interval(2, 3, True)) == Interval(1, 3)
    assert Union(Interval(1, 3), Interval(2, 4)) == Interval(1, 4)
    assert Union(Interval(1, 2), Interval(1, 3)) == Interval(1, 3)
    assert Union(Interval(1, 3), Interval(1, 2)) == Interval(1, 3)
    assert Union(Interval(1, 3, False, True), Interval(1, 2)) == \
        Interval(1, 3, False, True)
    assert Union(Interval(1, 3), Interval(1, 2, False, True)) == Interval(1, 3)
    assert Union(Interval(1, 2, True), Interval(1, 3)) == Interval(1, 3)
    assert Union(Interval(1, 2, True), Interval(1, 3, True)) == \
        Interval(1, 3, True)
    assert Union(Interval(1, 2, True), Interval(1, 3, True, True)) == \
        Interval(1, 3, True, True)
    assert Union(Interval(1, 2, True, True), Interval(1, 3, True)) == \
        Interval(1, 3, True)
    assert Union(Interval(1, 3), Interval(2, 3)) == Interval(1, 3)
    assert Union(Interval(1, 3, False, True), Interval(2, 3)) == \
        Interval(1, 3)
    assert Union(Interval(1, 2, False, True), Interval(2, 3, True)) != \
        Interval(1, 3)
    assert Union(Interval(1, 2), S.EmptySet) == Interval(1, 2)
    assert Union(S.EmptySet) == S.EmptySet

    assert Union(Interval(0, 1), *[FiniteSet(1.0/n) for n in range(1, 10)]) == \
        Interval(0, 1)
    # issue #18241:
    x = Symbol('x')
    assert Union(Interval(0, 1), FiniteSet(1, x)) == Union(
        Interval(0, 1), FiniteSet(x))
    assert unchanged(Union, Interval(0, 1), FiniteSet(2, x))

    assert Interval(1, 2).union(Interval(2, 3)) == \
        Interval(1, 2) + Interval(2, 3)

    assert Interval(1, 2).union(Interval(2, 3)) == Interval(1, 3)

    assert Union(Set()) == Set()

    assert FiniteSet(1) + FiniteSet(2) + FiniteSet(3) == FiniteSet(1, 2, 3)
    assert FiniteSet('ham') + FiniteSet('eggs') == FiniteSet('ham', 'eggs')
    assert FiniteSet(1, 2, 3) + S.EmptySet == FiniteSet(1, 2, 3)

    assert FiniteSet(1, 2, 3) & FiniteSet(2, 3, 4) == FiniteSet(2, 3)
    assert FiniteSet(1, 2, 3) | FiniteSet(2, 3, 4) == FiniteSet(1, 2, 3, 4)

    assert FiniteSet(1, 2, 3) & S.EmptySet == S.EmptySet
    assert FiniteSet(1, 2, 3) | S.EmptySet == FiniteSet(1, 2, 3)

    x = Symbol("x")
    y = Symbol("y")
    z = Symbol("z")
    assert S.EmptySet | FiniteSet(x, FiniteSet(y, z)) == \
        FiniteSet(x, FiniteSet(y, z))

    # Test that Intervals and FiniteSets play nicely
    assert Interval(1, 3) + FiniteSet(2) == Interval(1, 3)
    assert Interval(1, 3, True, True) + FiniteSet(3) == \
        Interval(1, 3, True, False)
    X = Interval(1, 3) + FiniteSet(5)
    Y = Interval(1, 2) + FiniteSet(3)
    XandY = X.intersect(Y)
    assert 2 in X and 3 in X and 3 in XandY
    assert XandY.is_subset(X) and XandY.is_subset(Y)

    raises(TypeError, lambda: Union(1, 2, 3))

    assert X.is_iterable is False

    # issue 7843
    assert Union(S.EmptySet, FiniteSet(-sqrt(-I), sqrt(-I))) == \
        FiniteSet(-sqrt(-I), sqrt(-I))

    assert Union(S.Reals, S.Integers) == S.Reals


def test_union():
    vx, vy = Variable(x, type=float64), Variable(y, type=int64)
    u = union('dualuse', [vx, vy])
    assert u.func(*u.args) == u
    assert u == union('dualuse', (vx, vy))
    assert str(u.name) == 'dualuse'
    assert len(u.declarations) == 2
    assert all(isinstance(arg, Declaration) for arg in u.declarations)
    assert ccode(u) == (
        "union dualuse {\n"
        "   double x;\n"
        "   int64_t y;\n"
        "}")


def test_union(idx, sort):
    piece1 = idx[:5][::-1]
    piece2 = idx[3:]

    the_union = piece1.union(piece2, sort=sort)

    if sort in (None, False):
        tm.assert_index_equal(the_union.sort_values(), idx.sort_values())
    else:
        tm.assert_index_equal(the_union, idx)

    # corner case, pass self or empty thing:
    the_union = idx.union(idx, sort=sort)
    tm.assert_index_equal(the_union, idx)

    the_union = idx.union(idx[:0], sort=sort)
    tm.assert_index_equal(the_union, idx)

    tuples = idx.values
    result = idx[:4].union(tuples[4:], sort=sort)
    if sort is None:
        tm.assert_index_equal(result.sort_values(), idx.sort_values())
    else:
        assert result.equals(idx)

