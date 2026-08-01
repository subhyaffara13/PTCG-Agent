
def test_imag_real():
    f_re = lambdify([z], sympy.re(z))
    val = 3+2j
    assert f_re(val) == val.real

    f_im = lambdify([z], sympy.im(z))  # see #15400
    assert f_im(val) == val.imag

