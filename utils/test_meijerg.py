
def test_meijerg():
    # carefully set up the parameters.
    # NOTE: this used to fail sometimes. I believe it is fixed, but if you
    #       hit an inexplicable test failure here, please let me know the seed.
    a1, a2 = (randcplx(n) - 5*I - n*I for n in range(2))
    b1, b2 = (randcplx(n) + 5*I + n*I for n in range(2))
    b3, b4, b5, a3, a4, a5 = (randcplx() for n in range(6))
    g = meijerg([a1], [a3, a4], [b1], [b3, b4], z)

    assert ReduceOrder.meijer_minus(3, 4) is None
    assert ReduceOrder.meijer_plus(4, 3) is None

    g2 = meijerg([a1, a2], [a3, a4], [b1], [b3, b4, a2], z)
    assert tn(ReduceOrder.meijer_plus(a2, a2).apply(g, op), g2, z)

    g2 = meijerg([a1, a2], [a3, a4], [b1], [b3, b4, a2 + 1], z)
    assert tn(ReduceOrder.meijer_plus(a2, a2 + 1).apply(g, op), g2, z)

    g2 = meijerg([a1, a2 - 1], [a3, a4], [b1], [b3, b4, a2 + 2], z)
    assert tn(ReduceOrder.meijer_plus(a2 - 1, a2 + 2).apply(g, op), g2, z)

    g2 = meijerg([a1], [a3, a4, b2 - 1], [b1, b2 + 2], [b3, b4], z)
    assert tn(ReduceOrder.meijer_minus(
        b2 + 2, b2 - 1).apply(g, op), g2, z, tol=1e-6)

    # test several-step reduction
    an = [a1, a2]
    bq = [b3, b4, a2 + 1]
    ap = [a3, a4, b2 - 1]
    bm = [b1, b2 + 1]
    niq, ops = reduce_order_meijer(G_Function(an, ap, bm, bq))
    assert niq.an == (a1,)
    assert set(niq.ap) == {a3, a4}
    assert niq.bm == (b1,)
    assert set(niq.bq) == {b3, b4}
    assert tn(apply_operators(g, ops, op), meijerg(an, ap, bm, bq, z), z)


def test_meijerg():
    expr = meijerg([pi, pi, x], [1], [0, 1], [1, 2, 3], z)
    ucode_str = \
"""\
╭─╮2, 3 ⎛π, π, x     1    │  ⎞\n\
│╶┐     ⎜                 │ z⎟\n\
╰─╯4, 5 ⎝ 0, 1    1, 2, 3 │  ⎠\
"""
    ascii_str = \
"""\
 __2, 3 /pi, pi, x     1    |  \\\n\
/__     |                   | z|\n\
\\_|4, 5 \\  0, 1     1, 2, 3 |  /\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = meijerg([1, pi/7], [2, pi, 5], [], [], z**2)
    ucode_str = \
"""\
        ⎛   π          │   ⎞\n\
╭─╮0, 2 ⎜1, ─  2, 5, π │  2⎟\n\
│╶┐     ⎜   7          │ z ⎟\n\
╰─╯5, 0 ⎜              │   ⎟\n\
        ⎝              │   ⎠\
"""
    ascii_str = \
"""\
        /   pi           |   \\\n\
 __0, 2 |1, --  2, 5, pi |  2|\n\
/__     |   7            | z |\n\
\\_|5, 0 |                |   |\n\
        \\                |   /\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    ucode_str = \
"""\
╭─╮ 1, 10 ⎛1, 1, 1, 1, 1, 1, 1, 1, 1, 1  1 │  ⎞\n\
│╶┐       ⎜                                │ z⎟\n\
╰─╯11,  2 ⎝             1                1 │  ⎠\
"""
    ascii_str = \
"""\
 __ 1, 10 /1, 1, 1, 1, 1, 1, 1, 1, 1, 1  1 |  \\\n\
/__       |                                | z|\n\
\\_|11,  2 \\             1                1 |  /\
"""

    expr = meijerg([1]*10, [1], [1], [1], z)
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = meijerg([1, 2, ], [4, 3], [3], [4, 5], 1/(1/(1/(1/x + 1) + 1) + 1))

    ucode_str = \
"""\
        ⎛           │       1      ⎞\n\
        ⎜           │ ─────────────⎟\n\
        ⎜           │         1    ⎟\n\
╭─╮1, 2 ⎜1, 2  3, 4 │ 1 + ─────────⎟\n\
│╶┐     ⎜           │           1  ⎟\n\
╰─╯4, 3 ⎜ 3    4, 5 │     1 + ─────⎟\n\
        ⎜           │             1⎟\n\
        ⎜           │         1 + ─⎟\n\
        ⎝           │             x⎠\
"""

    ascii_str = \
"""\
        /           |       1      \\\n\
        |           | -------------|\n\
        |           |         1    |\n\
 __1, 2 |1, 2  3, 4 | 1 + ---------|\n\
/__     |           |           1  |\n\
\\_|4, 3 | 3    4, 5 |     1 + -----|\n\
        |           |             1|\n\
        |           |         1 + -|\n\
        \\           |             x/\
"""

    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Integral(expr, x)

    ucode_str = \
"""\
⌠                                        \n\
⎮         ⎛           │       1      ⎞   \n\
⎮         ⎜           │ ─────────────⎟   \n\
⎮         ⎜           │         1    ⎟   \n\
⎮ ╭─╮1, 2 ⎜1, 2  3, 4 │ 1 + ─────────⎟   \n\
⎮ │╶┐     ⎜           │           1  ⎟ dx\n\
⎮ ╰─╯4, 3 ⎜ 3    4, 5 │     1 + ─────⎟   \n\
⎮         ⎜           │             1⎟   \n\
⎮         ⎜           │         1 + ─⎟   \n\
⎮         ⎝           │             x⎠   \n\
⌡                                        \
"""

    ascii_str = \
"""\
  /                                       \n\
 |                                        \n\
 |         /           |       1      \\   \n\
 |         |           | -------------|   \n\
 |         |           |         1    |   \n\
 |  __1, 2 |1, 2  3, 4 | 1 + ---------|   \n\
 | /__     |           |           1  | dx\n\
 | \\_|4, 3 | 3    4, 5 |     1 + -----|   \n\
 |         |           |             1|   \n\
 |         |           |         1 + -|   \n\
 |         \\           |             x/   \n\
 |                                        \n\
/                                         \
"""

    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str


def test_meijerg():
    mp.dps = 15
    assert meijerg([[2,3],[1]],[[0.5,2],[3,4]], 2.5).ae(4.2181028074787439386)
    assert meijerg([[],[1+j]],[[1],[1]], 3+4j).ae(271.46290321152464592 - 703.03330399954820169j)
    assert meijerg([[0.25],[1]],[[0.5],[2]],0) == 0
    assert meijerg([[0],[]],[[0,0,'1/3','2/3'], []], '2/27').ae(2.2019391389653314120)
    # Verify 1/z series being used
    assert meijerg([[-3],[-0.5]], [[-1],[-2.5]], -0.5).ae(-1.338096165935754898687431)
    assert meijerg([[1-(-1)],[1-(-2.5)]], [[1-(-3)],[1-(-0.5)]], -2.0).ae(-1.338096165935754898687431)
    assert meijerg([[-3],[-0.5]], [[-1],[-2.5]], -1).ae(-(pi+4)/(4*pi))
    a = 2.5
    b = 1.25
    for z in [mpf(0.25), mpf(2)]:
        x1 = hyp1f1(a,b,z)
        x2 = gamma(b)/gamma(a)*meijerg([[1-a],[]],[[0],[1-b]],-z)
        x3 = gamma(b)/gamma(a)*meijerg([[1-0],[1-(1-b)]],[[1-(1-a)],[]],-1/z)
        assert x1.ae(x2)
        assert x1.ae(x3)

