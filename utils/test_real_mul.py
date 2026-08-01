
def test_real_mul():
    assert Float(0) * pi * x == 0
    assert set((Float(1) * pi * x).args) == {Float(1), pi, x}

