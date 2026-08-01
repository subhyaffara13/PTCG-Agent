
def test_issue_18449():
    x, y, z = symbols("x, y, z")
    f = (x**2 + y**2)**2 + (x**2 + z**2)**2 - 2*(2*x**2 + y**2 + z**2)
    fx = diff(f, x)
    fy = diff(f, y)
    fz = diff(f, z)
    sol = nonlinsolve([fx, fy, fz], [x, y, z])
    for (xs, ys, zs) in sol:
        d = {x: xs, y: ys, z: zs}
        assert tuple(_.subs(d).simplify() for _ in (fx, fy, fz)) == (0, 0, 0)

