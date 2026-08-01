
def test_cyclic_parts():
    f = cos(x)*exp(x/4)
    F = 16*exp(x/4)*sin(x)/17 + 4*exp(x/4)*cos(x)/17
    assert manualintegrate(f, x) == F and F.diff(x) == f
    f = x*cos(x)*exp(x/4)
    F = (x*(16*exp(x/4)*sin(x)/17 + 4*exp(x/4)*cos(x)/17) -
        128*exp(x/4)*sin(x)/289 + 240*exp(x/4)*cos(x)/289)
    assert manualintegrate(f, x) == F and F.diff(x) == f

