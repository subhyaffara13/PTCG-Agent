
def test_cot_expansion():
    assert cot(x + y).expand(trig=True).together() == (
        (cot(x)*cot(y) - 1)/(cot(x) + cot(y)))
    assert cot(x - y).expand(trig=True).together() == (
        cot(x)*cot(-y) - 1)/(cot(x) + cot(-y))
    assert cot(x + y + z).expand(trig=True).together() == (
        (cot(x)*cot(y)*cot(z) - cot(x) - cot(y) - cot(z))/
        (-1 + cot(x)*cot(y) + cot(x)*cot(z) + cot(y)*cot(z)))
    assert cot(3*x).expand(trig=True).together() == (
        (cot(x)**2 - 3)*cot(x)/(3*cot(x)**2 - 1))
    assert cot(2*x).expand(trig=True) == cot(x)/2 - 1/(2*cot(x))
    assert cot(3*x).expand(trig=True).together() == (
        cot(x)**2 - 3)*cot(x)/(3*cot(x)**2 - 1)
    assert cot(4*x - pi/4).expand(trig=True).cancel() == (
        -tan(x)**4 + 4*tan(x)**3 + 6*tan(x)**2 - 4*tan(x) - 1
        )/(tan(x)**4 + 4*tan(x)**3 - 6*tan(x)**2 - 4*tan(x) + 1)
    _test_extrig(cot, 2, (-1 + cot(1)**2)/(2*cot(1)))
    _test_extrig(cot, 3, (-3*cot(1) + cot(1)**3)/(-1 + 3*cot(1)**2))

