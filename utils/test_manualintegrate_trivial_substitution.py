
def test_manualintegrate_trivial_substitution():
    assert manualintegrate((exp(x) - exp(-x))/x, x) == -Ei(-x) + Ei(x)
    f = Function('f')
    assert manualintegrate((f(x) - f(-x))/x, x) == \
        -Integral(f(-x)/x, x) + Integral(f(x)/x, x)

