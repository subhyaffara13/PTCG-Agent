
def test_array_newton_failures():
    """Test that array newton fails as expected"""
    # p = 0.68  # [MPa]
    # dp = -0.068 * 1e6  # [Pa]
    # T = 323  # [K]
    diameter = 0.10  # [m]
    # L = 100  # [m]
    roughness = 0.00015  # [m]
    rho = 988.1  # [kg/m**3]
    mu = 5.4790e-04  # [Pa*s]
    u = 2.488  # [m/s]
    reynolds_number = rho * u * diameter / mu  # Reynolds number

    def colebrook_eqn(darcy_friction, re, dia):
        return (1 / np.sqrt(darcy_friction) +
                2 * np.log10(roughness / 3.7 / dia +
                             2.51 / re / np.sqrt(darcy_friction)))

    # only some failures
    with pytest.warns(RuntimeWarning):
        result = zeros.newton(
            colebrook_eqn, x0=[0.01, 0.2, 0.02223, 0.3], maxiter=2,
            args=[reynolds_number, diameter], full_output=True
        )
        assert not result.converged.all()
    # they all fail
    with pytest.raises(RuntimeError):
        result = zeros.newton(
            colebrook_eqn, x0=[0.01] * 2, maxiter=2,
            args=[reynolds_number, diameter], full_output=True
        )

