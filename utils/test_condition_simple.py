
def test_condition_simple():
    rl = rewriterule(x, x+1, [x], lambda x: x < 10)
    assert not list(rl(S(15)))
    assert rebuild(next(rl(S(5)))) == 6

