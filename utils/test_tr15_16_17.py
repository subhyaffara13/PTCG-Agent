
def test_TR15_16_17():
    assert TR15(1 - 1/sin(x)**2) == -cot(x)**2
    assert TR16(1 - 1/cos(x)**2) == -tan(x)**2
    assert TR111(1 - 1/tan(x)**2) == 1 - cot(x)**2

