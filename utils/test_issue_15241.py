
def test_issue_15241():
    F = f(x)
    Fx = F.diff(x)
    assert (F + x*Fx).diff(x, Fx) == 2
    assert (F + x*Fx).diff(Fx, x) == 1
    assert (x*F + x*Fx*F).diff(F, x) == x*Fx.diff(x) + Fx + 1
    assert (x*F + x*Fx*F).diff(x, F) == x*Fx.diff(x) + Fx + 1
    y = f(x)
    G = f(y)
    Gy = G.diff(y)
    assert (G + y*Gy).diff(y, Gy) == 2
    assert (G + y*Gy).diff(Gy, y) == 1
    assert (y*G + y*Gy*G).diff(G, y) == y*Gy.diff(y) + Gy + 1
    assert (y*G + y*Gy*G).diff(y, G) == y*Gy.diff(y) + Gy + 1

