
def test_Y10():
    assert (fourier_transform(abs(x)*exp(-3*abs(x)), x, z).cancel() ==
            (-8*pi**2*z**2 + 18)/(16*pi**4*z**4 + 72*pi**2*z**2 + 81))

