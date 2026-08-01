
def test_issue_4886():
    z = a*sqrt(R**2*a**2 + R**2*b**2 - c**2)/(a**2 + b**2)
    t = b*c/(a**2 + b**2)
    sol = [((b*(t - z) - c)/(-a), t - z), ((b*(t + z) - c)/(-a), t + z)]
    assert solve([x**2 + y**2 - R**2, a*x + b*y - c], x, y) == sol

