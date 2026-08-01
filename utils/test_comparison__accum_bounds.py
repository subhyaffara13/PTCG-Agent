
def test_comparison_AccumBounds():
    assert (B(1, 3) < 4) == S.true
    assert (B(1, 3) < -1) == S.false
    assert (B(1, 3) < 2).rel_op == '<'
    assert (B(1, 3) <= 2).rel_op == '<='

    assert (B(1, 3) > 4) == S.false
    assert (B(1, 3) > -1) == S.true
    assert (B(1, 3) > 2).rel_op == '>'
    assert (B(1, 3) >= 2).rel_op == '>='

    assert (B(1, 3) < B(4, 6)) == S.true
    assert (B(1, 3) < B(2, 4)).rel_op == '<'
    assert (B(1, 3) < B(-2, 0)) == S.false

    assert (B(1, 3) <= B(4, 6)) == S.true
    assert (B(1, 3) <= B(-2, 0)) == S.false

    assert (B(1, 3) > B(4, 6)) == S.false
    assert (B(1, 3) > B(-2, 0)) == S.true

    assert (B(1, 3) >= B(4, 6)) == S.false
    assert (B(1, 3) >= B(-2, 0)) == S.true

    # issue 13499
    assert (cos(x) > 0).subs(x, oo) == (B(-1, 1) > 0)

    c = Symbol('c')
    raises(TypeError, lambda: (B(0, 1) < c))
    raises(TypeError, lambda: (B(0, 1) <= c))
    raises(TypeError, lambda: (B(0, 1) > c))
    raises(TypeError, lambda: (B(0, 1) >= c))

