
def test_issue_5236():
    assert (cos(1 + I)**3).as_real_imag() == (-3*sin(1)**2*sinh(1)**2*cos(1)*cosh(1) +
        cos(1)**3*cosh(1)**3, -3*cos(1)**2*cosh(1)**2*sin(1)*sinh(1) + sin(1)**3*sinh(1)**3)

