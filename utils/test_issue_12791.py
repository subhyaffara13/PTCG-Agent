
def test_issue_12791():
    beta = symbols('beta', positive=True)
    theta, varphi = symbols('theta varphi', real=True)

    expr = (-beta**2*varphi*sin(theta) + beta**2*cos(theta) + \
        beta*varphi*sin(theta) - beta*cos(theta) - beta + 1)/(beta*cos(theta) - 1)**2

    sol = (0.5/(0.5*cos(theta) - 1.0)**2 - 0.25*cos(theta)/(0.5*cos(theta) - 1.0)**2
        + (beta - 0.5)*(-0.25*varphi*sin(2*theta) - 1.5*cos(theta)
        + 0.25*cos(2*theta) + 1.25)/((0.5*cos(theta) - 1.0)**2*(0.5*cos(theta) - 1.0))
        + 0.25*varphi*sin(theta)/(0.5*cos(theta) - 1.0)**2
        + O((beta - S.Half)**2, (beta, S.Half)))

    assert expr.series(beta, 0.5, 2).trigsimp() == sol

