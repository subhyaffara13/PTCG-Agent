
def test_radsimp_issue_3214():
    c, p = symbols('c p', positive=True)
    s = sqrt(c**2 - p**2)
    b = (c + I*p - s)/(c + I*p + s)
    assert radsimp(b) == -I*(c + I*p - sqrt(c**2 - p**2))**2/(2*c*p)

