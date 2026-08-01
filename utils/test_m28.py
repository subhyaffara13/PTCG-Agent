
def test_M28():
    assert solveset_real(5*x + exp((x - 5)/2) - 8*x**3, x, assume=Q.real(x)) == [-0.784966, -0.016291, 0.802557]

