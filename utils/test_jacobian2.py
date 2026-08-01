
def test_jacobian2():
    rho, phi = symbols("rho,phi")
    X = Matrix([rho * cos(phi), rho * sin(phi), rho ** 2])
    Y = Matrix([rho, phi])
    J = Matrix([
        [cos(phi), -rho * sin(phi)],
        [sin(phi), rho * cos(phi)],
        [2 * rho, 0],
    ])
    assert _forward_jacobian(X, Y) == J


def test_jacobian2():
    rho, phi = symbols("rho,phi")
    X = CalculusOnlyMatrix(3, 1, [rho*cos(phi), rho*sin(phi), rho**2])
    Y = CalculusOnlyMatrix(2, 1, [rho, phi])
    J = Matrix([
        [cos(phi), -rho*sin(phi)],
        [sin(phi),  rho*cos(phi)],
        [   2*rho,             0],
    ])
    assert X.jacobian(Y) == J

    m = CalculusOnlyMatrix(2, 2, [1, 2, 3, 4])
    m2 = CalculusOnlyMatrix(4, 1, [1, 2, 3, 4])
    raises(TypeError, lambda: m.jacobian(Matrix([1, 2])))
    raises(TypeError, lambda: m2.jacobian(m))


def test_jacobian2():
    rho, phi = symbols("rho,phi")
    X = Matrix([rho*cos(phi), rho*sin(phi), rho**2])
    Y = Matrix([rho, phi])
    J = Matrix([
        [cos(phi), -rho*sin(phi)],
        [sin(phi),  rho*cos(phi)],
        [   2*rho,             0],
    ])
    assert X.jacobian(Y) == J


def test_jacobian2():
    rho, phi = symbols("rho,phi")
    X = Matrix([rho*cos(phi), rho*sin(phi), rho**2])
    Y = Matrix([rho, phi])
    J = Matrix([
        [cos(phi), -rho*sin(phi)],
        [sin(phi),  rho*cos(phi)],
        [   2*rho,             0],
    ])
    assert X.jacobian(Y) == J

