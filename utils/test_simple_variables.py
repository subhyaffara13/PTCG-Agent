
def test_simple_variables():
    rl = rewriterule(Basic(x, S(1)), Basic(x, S(2)), variables=(x,))
    assert list(rl(Basic(S(3), S(1)))) == [Basic(S(3), S(2))]

    rl = rewriterule(x**2, x**3, variables=(x,))
    assert list(rl(y**2)) == [y**3]

