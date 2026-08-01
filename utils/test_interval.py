
def test_interval():
    assert (interval(1, 1) == interval(1, 1, is_valid=True)) == (True, True)
    assert (interval(1, 1) == interval(1, 1, is_valid=False)) == (True, False)
    assert (interval(1, 1) == interval(1, 1, is_valid=None)) == (True, None)
    assert (interval(1, 1.5) == interval(1, 2)) == (None, True)
    assert (interval(0, 1) == interval(2, 3)) == (False, True)
    assert (interval(0, 1) == interval(1, 2)) == (None, True)
    assert (interval(1, 2) != interval(1, 2)) == (False, True)
    assert (interval(1, 3) != interval(2, 3)) == (None, True)
    assert (interval(1, 3) != interval(-5, -3)) == (True, True)
    assert (
        interval(1, 3, is_valid=False) != interval(-5, -3)) == (True, False)
    assert (interval(1, 3, is_valid=None) != interval(-5, 3)) == (None, None)
    assert (interval(4, 4) != 4) == (False, True)
    assert (interval(1, 1) == 1) == (True, True)
    assert (interval(1, 3, is_valid=False) == interval(1, 3)) == (True, False)
    assert (interval(1, 3, is_valid=None) == interval(1, 3)) == (True, None)
    inter = interval(-5, 5)
    assert (interval(inter) == interval(-5, 5)) == (True, True)
    assert inter.width == 10
    assert 0 in inter
    assert -5 in inter
    assert 5 in inter
    assert interval(0, 3) in inter
    assert interval(-6, 2) not in inter
    assert -5.05 not in inter
    assert 5.3 not in inter
    interb = interval(-float('inf'), float('inf'))
    assert 0 in inter
    assert inter in interb
    assert interval(0, float('inf')) in interb
    assert interval(-float('inf'), 5) in interb
    assert interval(-1e50, 1e50) in interb
    assert (
        -interval(-1, -2, is_valid=False) == interval(1, 2)) == (True, False)
    raises(ValueError, lambda: interval(1, 2, 3))


def test_interval(distname, shapes):
    # gh-11026 reported that `interval` returns incorrect values when
    # `confidence=1`. The values were not incorrect, but it was not intuitive
    # that the left end of the interval should extend beyond the support of the
    # distribution. Confirm that this is the behavior for all distributions.
    if isinstance(distname, str):
        dist = getattr(stats, distname)
    else:
        dist = distname
    a, b = dist.support(*shapes)
    npt.assert_equal(dist.ppf([0, 1], *shapes), (a-1, b))
    npt.assert_equal(dist.isf([1, 0], *shapes), (a-1, b))
    npt.assert_equal(dist.interval(1, *shapes), (a-1, b))

