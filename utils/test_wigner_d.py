
def test_wigner_d():
    half = S(1)/2
    assert wigner_d_small(half, 0) == Matrix([[1, 0], [0, 1]])
    assert wigner_d_small(half, pi/2) == Matrix([[1, 1], [-1, 1]])/sqrt(2)
    assert wigner_d_small(half, pi) == Matrix([[0, 1], [-1, 0]])

    alpha, beta, gamma = symbols("alpha, beta, gamma", real=True)
    D = wigner_d(half, alpha, beta, gamma)
    assert D[0, 0] == exp(I*alpha/2)*exp(I*gamma/2)*cos(beta/2)
    assert D[0, 1] == exp(I*alpha/2)*exp(-I*gamma/2)*sin(beta/2)
    assert D[1, 0] == -exp(-I*alpha/2)*exp(I*gamma/2)*sin(beta/2)
    assert D[1, 1] == exp(-I*alpha/2)*exp(-I*gamma/2)*cos(beta/2)

    # Test Y_{n mi}(g*x)=\sum_{mj}D^n_{mi mj}*Y_{n mj}(x)
    theta, phi = symbols("theta phi", real=True)
    v = Matrix([Ynm(1, mj, theta, phi) for mj in range(1, -2, -1)])
    w = wigner_d(1, -pi/2, pi/2, -pi/2)@v.subs({theta: pi/4, phi: pi})
    w_ = v.subs({theta: pi/2, phi: pi/4})
    assert w.expand(func=True).as_real_imag() == w_.expand(func=True).as_real_imag()


def test_wignerD():
    i,j=symbols('i j')
    assert Rotation.D(1, 1, 1, 0, 0, 0) == WignerD(1, 1, 1, 0, 0, 0)
    assert Rotation.D(1, 1, 2, 0, 0, 0) == WignerD(1, 1, 2, 0, 0, 0)
    assert Rotation.D(1, i**2 - j**2, i**2 - j**2, 0, 0, 0) == WignerD(1, i**2 - j**2, i**2 - j**2, 0, 0, 0)
    assert Rotation.D(1, i, i, 0, 0, 0) == WignerD(1, i, i, 0, 0, 0)
    assert Rotation.D(1, i, i+1, 0, 0, 0) == WignerD(1, i, i+1, 0, 0, 0)
    assert Rotation.D(1, 0, 0, 0, 0, 0) == WignerD(1, 0, 0, 0, 0, 0)

