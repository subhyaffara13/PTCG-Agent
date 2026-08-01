
def test_issue_21831():
    theta = symbols('theta')
    assert integrate(cos(3*theta)/(5-4*cos(theta)), (theta, 0, 2*pi)) == pi/12
    integrand = cos(2*theta)/(5 - 4*cos(theta))
    assert integrate(integrand, (theta, 0, 2*pi)) == pi/6

