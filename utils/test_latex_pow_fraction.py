
def test_latex_pow_fraction():
    x = Symbol('x')
    # Testing exp
    assert r'e^{-x}' in latex(exp(-x)/2).replace(' ', '')  # Remove Whitespace

    # Testing e^{-x} in case future changes alter behavior of muls or fracs
    # In particular current output is \frac{1}{2}e^{- x} but perhaps this will
    # change to \frac{e^{-x}}{2}

    # Testing general, non-exp, power
    assert r'3^{-x}' in latex(3**-x/2).replace(' ', '')

