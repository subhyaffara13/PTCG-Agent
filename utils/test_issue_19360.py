
def test_issue_19360():
    f = 2*x**2 - 2*sqrt(2)*x*y + y**2
    assert factor(f, extension=sqrt(2)) == 2*(x - (sqrt(2)*y/2))**2

    f = -I*t*x - t*y + x*z - I*y*z
    assert factor(f, extension=I) == (x - I*y)*(-I*t + z)

