
def test_recognize_derivative():
    DE = DifferentialExtension(extension={'D': [Poly(1, t)]})
    a = Poly(36, t)
    d = Poly((t - 2)*(t**2 - 1)**2, t)
    assert recognize_derivative(a, d, DE) == False
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(1/x, t)]})
    a = Poly(2, t)
    d = Poly(t**2 - 1, t)
    assert recognize_derivative(a, d, DE) == False
    assert recognize_derivative(Poly(x*t, t), Poly(1, t), DE) == True
    DE = DifferentialExtension(extension={'D': [Poly(1, x), Poly(t**2 + 1, t)]})
    assert recognize_derivative(Poly(t, t), Poly(1, t), DE) == True

