
def test_TransferFunction_phase_margin():
    # Test for phase margin
    tf1 = TransferFunction(10, p**3 + 1, p)
    tf2 = TransferFunction(s**2, 10, s)
    tf3 = TransferFunction(1, a*s+b, s)
    tf4 = TransferFunction((s + 1)*exp(s/tau), s**2 + 2, s)
    tf_m = TransferFunctionMatrix([[tf2],[tf3]])

    assert phase_margin(tf1) == -180 + 180*atan(3*sqrt(11))/pi
    assert phase_margin(tf2) == 0

    raises(NotImplementedError, lambda: phase_margin(tf4))
    raises(ValueError, lambda: phase_margin(tf3))
    raises(ValueError, lambda: phase_margin(MIMOSeries(tf_m)))

