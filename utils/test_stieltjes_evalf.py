
def test_stieltjes_evalf():
    assert abs(stieltjes(0).evalf() - 0.577215664) < 1E-9
    assert abs(stieltjes(0, 0.5).evalf() - 1.963510026) < 1E-9
    assert abs(stieltjes(1, 2).evalf() + 0.072815845) < 1E-9

