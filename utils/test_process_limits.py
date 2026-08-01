
def test_process_limits():
    from sympy.concrete.expr_with_limits import _process_limits

    # these should be (x, Range(3)) not Range(3)
    raises(ValueError, lambda: _process_limits(
        Range(3), discrete=True))
    raises(ValueError, lambda: _process_limits(
        Range(3), discrete=False))
    # these should be (x, union) not union
    # (but then we would get a TypeError because we don't
    # handle non-contiguous sets: see below use of `union`)
    union = Or(x < 1, x > 3).as_set()
    raises(ValueError, lambda: _process_limits(
        union, discrete=True))
    raises(ValueError, lambda: _process_limits(
        union, discrete=False))

    # error not triggered if not needed
    assert _process_limits((x, 1, 2)) == ([(x, 1, 2)], 1)

    # this equivalence is used to detect Reals in _process_limits
    assert isinstance(S.Reals, Interval)

    C = Integral  # continuous limits
    assert C(x, x >= 5) == C(x, (x, 5, oo))
    assert C(x, x < 3) == C(x, (x, -oo, 3))
    ans = C(x, (x, 0, 3))
    assert C(x, And(x >= 0, x < 3)) == ans
    assert C(x, (x, Interval.Ropen(0, 3))) == ans
    raises(TypeError, lambda: C(x, (x, Range(3))))

    # discrete limits
    for D in (Sum, Product):
        r, ans = Range(3, 10, 2), D(2*x + 3, (x, 0, 3))
        assert D(x, (x, r)) == ans
        assert D(x, (x, r.reversed)) == ans
        r, ans = Range(3, oo, 2), D(2*x + 3, (x, 0, oo))
        assert D(x, (x, r)) == ans
        assert D(x, (x, r.reversed)) == ans
        r, ans = Range(-oo, 5, 2), D(3 - 2*x, (x, 0, oo))
        assert D(x, (x, r)) == ans
        assert D(x, (x, r.reversed)) == ans
        raises(TypeError, lambda: D(x, x > 0))
        raises(ValueError, lambda: D(x, Interval(1, 3)))
        raises(NotImplementedError, lambda: D(x, (x, union)))

