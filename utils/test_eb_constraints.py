
def test_eb_constraints():
    # make sure constraint functions aren't overwritten when equal bounds
    # are employed, and a parameter is factored out. GH14859
    def f(x):
        return x[0]**3 + x[1]**2 + x[2]*x[3]

    def cfun(x):
        return x[0] + x[1] + x[2] + x[3] - 40

    constraints = [{'type': 'ineq', 'fun': cfun}]

    bounds = [(0, 20)] * 4
    bounds[1] = (5, 5)
    optimize.minimize(
        f,
        x0=[1, 2, 3, 4],
        method='SLSQP',
        bounds=bounds,
        constraints=constraints,
    )
    assert constraints[0]['fun'] == cfun

