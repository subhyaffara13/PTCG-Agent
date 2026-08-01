
def test_recognize_log_derivative():

    a = Poly(2*x**2 + 4*x*t - 2*t - x**2*t, t)
    d = Poly((2*x + t)*(t + x**2), t)
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(t, t)]})
    assert recognize_log_derivative(a, d, DE, z) == True
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(1/x, t)]})
    assert recognize_log_derivative(Poly(t + 1, t), Poly(t + x, t), DE) == True
    assert recognize_log_derivative(Poly(2, t), Poly(t**2 - 1, t), DE) == True
    DE = DifferentialExtension(extension={'D': [Poly(1, x)]})
    assert recognize_log_derivative(Poly(1, x), Poly(x**2 - 2, x), DE) == False
    assert recognize_log_derivative(Poly(1, x), Poly(x**2 + x, x), DE) == True
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(t**2 + 1, t)]})
    assert recognize_log_derivative(Poly(1, t), Poly(t**2 - 2, t), DE) == False
    assert recognize_log_derivative(Poly(1, t), Poly(t**2 + t, t), DE) == False

