
def test_TransferFunction_gain_margin():
    # Test for gain margin
    tf1 = TransferFunction(s**2, 5*(s+1)*(s-5)*(s-10), s)
    tf2 = TransferFunction(s**2 + 2*s + 1, 1, s)
    tf3 = TransferFunction(1, a*s+b, s)
    tf4 = TransferFunction((s + 1)*exp(s/tau), s**2 + 2, s)
    tf_m = TransferFunctionMatrix([[tf2],[tf3]])

    assert gain_margin(tf1) == -20*log(S(7)/540)/log(10)
    assert gain_margin(tf2) == oo

    raises(NotImplementedError, lambda: gain_margin(tf4))
    raises(ValueError, lambda: gain_margin(tf3))
    raises(ValueError, lambda: gain_margin(MIMOSeries(tf_m)))

