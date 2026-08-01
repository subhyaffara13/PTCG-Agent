
def test_pmint_LambertW():
    f = LambertW(x)
    g = x*LambertW(x) - x + x/LambertW(x)

    assert heurisch(f, x) == g

