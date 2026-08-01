
def test_issue_17479():
    f = (x**2 + y**2)**2 + (x**2 + z**2)**2 - 2*(2*x**2 + y**2 + z**2)
    fx = f.diff(x)
    fy = f.diff(y)
    fz = f.diff(z)
    sol = nonlinsolve([fx, fy, fz], [x, y, z])
    assert len(sol) >= 4 and len(sol) <= 20

