
def test_sincos():
    p1 = sin(p)**2 + sin(p)**2
    p2 = 1
    rl = rewriterule(p1, p2, (p, q))

    assert list(rl(sin(x)**2 + sin(x)**2)) == [1]
    assert list(rl(sin(y)**2 + sin(y)**2)) == [1]

