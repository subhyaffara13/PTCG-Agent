
def test_factor_large():
    f = (x**2 + 4*x + 4)**10000000*(x**2 + 1)*(x**2 + 2*x + 1)**1234567
    g = ((x**2 + 2*x + 1)**3000*y**2 + (x**2 + 2*x + 1)**3000*2*y + (
        x**2 + 2*x + 1)**3000)

    assert factor(f) == (x + 2)**20000000*(x**2 + 1)*(x + 1)**2469134
    assert factor(g) == (x + 1)**6000*(y + 1)**2

    assert factor_list(
        f) == (1, [(x + 1, 2469134), (x + 2, 20000000), (x**2 + 1, 1)])
    assert factor_list(g) == (1, [(y + 1, 2), (x + 1, 6000)])

    f = (x**2 - y**2)**200000*(x**7 + 1)
    g = (x**2 + y**2)**200000*(x**7 + 1)

    assert factor(f) == \
        (x + 1)*(x - y)**200000*(x + y)**200000*(x**6 - x**5 +
         x**4 - x**3 + x**2 - x + 1)
    assert factor(g, gaussian=True) == \
        (x + 1)*(x - I*y)**200000*(x + I*y)**200000*(x**6 - x**5 +
         x**4 - x**3 + x**2 - x + 1)

    assert factor_list(f) == \
        (1, [(x + 1, 1), (x - y, 200000), (x + y, 200000), (x**6 -
         x**5 + x**4 - x**3 + x**2 - x + 1, 1)])
    assert factor_list(g, gaussian=True) == \
        (1, [(x + 1, 1), (x - I*y, 200000), (x + I*y, 200000), (
            x**6 - x**5 + x**4 - x**3 + x**2 - x + 1, 1)])

