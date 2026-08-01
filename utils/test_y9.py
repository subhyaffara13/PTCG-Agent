
def test_Y9():
    assert (fourier_transform(exp(-9*x**2), x, z) ==
            sqrt(pi)*exp(-pi**2*z**2/9)/3)

