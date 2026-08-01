
def test_sincos_rewrite_sqrt_257():
    assert cos(pi/257).rewrite(sqrt).evalf(64) == cos(pi/257).evalf(64)

