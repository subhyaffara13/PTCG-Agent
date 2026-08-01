
def test_density_constant():
    assert density(3)(2) == 0
    assert density(3)(3) == DiracDelta(0)

