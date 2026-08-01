
def test_TransferFunction_is_strictly_proper():
    omega_o, zeta, tau = symbols('omega_o, zeta, tau')
    tf1 = TransferFunction(omega_o**2, s**2 + p*omega_o*zeta*s + omega_o**2, omega_o)
    tf2 = TransferFunction(tau - s**3, tau + p**4, tau)
    tf3 = TransferFunction(a*b*s**3 + s**2 - a*p + s, b - s*p**2, p)
    tf4 = TransferFunction(b*s**2 + p**2 - a*p + s, b - p**2, s)
    assert not tf1.is_strictly_proper
    assert not tf2.is_strictly_proper
    assert tf3.is_strictly_proper
    assert not tf4.is_strictly_proper

