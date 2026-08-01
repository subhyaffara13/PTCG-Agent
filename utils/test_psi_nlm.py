
def test_psi_nlm():
    r=S('r')
    phi=S('phi')
    theta=S('theta')
    assert (Psi_nlm(1, 0, 0, r, phi, theta) == exp(-r) / sqrt(pi))
    assert (Psi_nlm(2, 1, -1, r, phi, theta)) == S.Half * exp(-r / (2)) * r \
        * (sin(theta) * exp(-I * phi) / (4 * sqrt(pi)))
    assert (Psi_nlm(3, 2, 1, r, phi, theta, 2) == -sqrt(2) * sin(theta) \
         * exp(I * phi) * cos(theta) / (4 * sqrt(pi)) * S(2) / 81 \
        * sqrt(2 * 2 ** 3) * exp(-2 * r / (3)) * (r * 2) ** 2)

