
def test_DifferentialExtension_all_attrs():
    # Test 'unimportant' attributes
    DE = DifferentialExtension(exp(x)*log(x), x, handle_first='exp')
    assert DE.f == exp(x)*log(x)
    assert DE.newf == t0*t1
    assert DE.x == x
    assert DE.cases == ['base', 'exp', 'primitive']
    assert DE.case == 'primitive'

    assert DE.level == -1
    assert DE.t == t1 == DE.T[DE.level]
    assert DE.d == Poly(1/x, t1) == DE.D[DE.level]
    raises(ValueError, lambda: DE.increment_level())
    DE.decrement_level()
    assert DE.level == -2
    assert DE.t == t0 == DE.T[DE.level]
    assert DE.d == Poly(t0, t0) == DE.D[DE.level]
    assert DE.case == 'exp'
    DE.decrement_level()
    assert DE.level == -3
    assert DE.t == x == DE.T[DE.level] == DE.x
    assert DE.d == Poly(1, x) == DE.D[DE.level]
    assert DE.case == 'base'
    raises(ValueError, lambda: DE.decrement_level())
    DE.increment_level()
    DE.increment_level()
    assert DE.level == -1
    assert DE.t == t1 == DE.T[DE.level]
    assert DE.d == Poly(1/x, t1) == DE.D[DE.level]
    assert DE.case == 'primitive'

    # Test methods
    assert DE.indices('log') == [2]
    assert DE.indices('exp') == [1]

