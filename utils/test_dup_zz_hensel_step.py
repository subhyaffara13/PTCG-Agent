
def test_dup_zz_hensel_step():
    R, x = ring("x", ZZ)

    f = x**4 - 1
    g = x**3 + 2*x**2 - x - 2
    h = x - 2
    s = -2
    t = 2*x**2 - 2*x - 1

    G, H, S, T = R.dup_zz_hensel_step(5, f, g, h, s, t)

    assert G == x**3 + 7*x**2 - x - 7
    assert H == x - 7
    assert S == 8
    assert T == -8*x**2 - 12*x - 1

