
def test_X18():
    # Power series (compute the general formula). Maple FPS:
    # > FormalPowerSeries(exp(-x)*sin(x), x = 0);
    #                        infinity
    #                         -----    (1/2 k)                k
    #                          \      2        sin(3/4 k Pi) x
    #                           )     -------------------------
    #                          /                 k!
    #                         -----
    #
    # Now, SymPy returns
    #      oo
    #    _____
    #    \    `
    #     \        /          k             k\
    #      \     k |I*(-1 - I)    I*(-1 + I) |
    #       \   x *|----------- - -----------|
    #       /      \     2             2     /
    #      /    ------------------------------
    #     /                   k!
    #    /____,
    #    k = 0
    k = Dummy('k')
    assert fps(exp(-x)*sin(x)) == \
        Sum(2**(S.Half*k)*sin(R(3, 4)*k*pi)*x**k/factorial(k), (k, 0, oo))

