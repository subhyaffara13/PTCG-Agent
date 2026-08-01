
def test_rotation_d():
    # Symbolic tests
    # j = 1/2
    assert Rotation.D(S.Half, S.Half, S.Half, alpha, beta, gamma).doit() == \
        cos(beta/2)*exp(-I*alpha/2)*exp(-I*gamma/2)
    assert Rotation.D(S.Half, S.Half, Rational(-1, 2), alpha, beta, gamma).doit() == \
        -sin(beta/2)*exp(-I*alpha/2)*exp(I*gamma/2)
    assert Rotation.D(S.Half, Rational(-1, 2), S.Half, alpha, beta, gamma).doit() == \
        sin(beta/2)*exp(I*alpha/2)*exp(-I*gamma/2)
    assert Rotation.D(S.Half, Rational(-1, 2), Rational(-1, 2), alpha, beta, gamma).doit() == \
        cos(beta/2)*exp(I*alpha/2)*exp(I*gamma/2)
    # j = 1
    assert Rotation.D(1, 1, 1, alpha, beta, gamma).doit() == \
        (1 + cos(beta))/2*exp(-I*alpha)*exp(-I*gamma)
    assert Rotation.D(1, 1, 0, alpha, beta, gamma).doit() == -sin(
        beta)/sqrt(2)*exp(-I*alpha)
    assert Rotation.D(1, 1, -1, alpha, beta, gamma).doit() == \
        (1 - cos(beta))/2*exp(-I*alpha)*exp(I*gamma)
    assert Rotation.D(1, 0, 1, alpha, beta, gamma).doit() == \
        sin(beta)/sqrt(2)*exp(-I*gamma)
    assert Rotation.D(1, 0, 0, alpha, beta, gamma).doit() == cos(beta)
    assert Rotation.D(1, 0, -1, alpha, beta, gamma).doit() == \
        -sin(beta)/sqrt(2)*exp(I*gamma)
    assert Rotation.D(1, -1, 1, alpha, beta, gamma).doit() == \
        (1 - cos(beta))/2*exp(I*alpha)*exp(-I*gamma)
    assert Rotation.D(1, -1, 0, alpha, beta, gamma).doit() == \
        sin(beta)/sqrt(2)*exp(I*alpha)
    assert Rotation.D(1, -1, -1, alpha, beta, gamma).doit() == \
        (1 + cos(beta))/2*exp(I*alpha)*exp(I*gamma)
    # j = 3/2
    assert Rotation.D(Rational(3, 2), Rational(3, 2), Rational(3, 2), alpha, beta, gamma).doit() == \
        (3*cos(beta/2) + cos(beta*Rational(3, 2)))/4*exp(I*alpha*Rational(-3, 2))*exp(I*gamma*Rational(-3, 2))
    assert Rotation.D(Rational(3, 2), Rational(3, 2), S.Half, alpha, beta, gamma).doit() == \
        -sqrt(3)*(sin(beta/2) + sin(beta*Rational(3, 2)))/4*exp(I*alpha*Rational(-3, 2))*exp(-I*gamma/2)
    assert Rotation.D(Rational(3, 2), Rational(3, 2), Rational(-1, 2), alpha, beta, gamma).doit() == \
        sqrt(3)*(cos(beta/2) - cos(beta*Rational(3, 2)))/4*exp(I*alpha*Rational(-3, 2))*exp(I*gamma/2)
    assert Rotation.D(Rational(3, 2), Rational(3, 2), Rational(-3, 2), alpha, beta, gamma).doit() == \
        (-3*sin(beta/2) + sin(beta*Rational(3, 2)))/4*exp(I*alpha*Rational(-3, 2))*exp(I*gamma*Rational(3, 2))
    assert Rotation.D(Rational(3, 2), S.Half, Rational(3, 2), alpha, beta, gamma).doit() == \
        sqrt(3)*(sin(beta/2) + sin(beta*Rational(3, 2)))/4*exp(-I*alpha/2)*exp(I*gamma*Rational(-3, 2))
    assert Rotation.D(Rational(3, 2), S.Half, S.Half, alpha, beta, gamma).doit() == \
        (cos(beta/2) + 3*cos(beta*Rational(3, 2)))/4*exp(-I*alpha/2)*exp(-I*gamma/2)
    assert Rotation.D(Rational(3, 2), S.Half, Rational(-1, 2), alpha, beta, gamma).doit() == \
        (sin(beta/2) - 3*sin(beta*Rational(3, 2)))/4*exp(-I*alpha/2)*exp(I*gamma/2)
    assert Rotation.D(Rational(3, 2), S.Half, Rational(-3, 2), alpha, beta, gamma).doit() == \
        sqrt(3)*(cos(beta/2) - cos(beta*Rational(3, 2)))/4*exp(-I*alpha/2)*exp(I*gamma*Rational(3, 2))
    assert Rotation.D(Rational(3, 2), Rational(-1, 2), Rational(3, 2), alpha, beta, gamma).doit() == \
        sqrt(3)*(cos(beta/2) - cos(beta*Rational(3, 2)))/4*exp(I*alpha/2)*exp(I*gamma*Rational(-3, 2))
    assert Rotation.D(Rational(3, 2), Rational(-1, 2), S.Half, alpha, beta, gamma).doit() == \
        (-sin(beta/2) + 3*sin(beta*Rational(3, 2)))/4*exp(I*alpha/2)*exp(-I*gamma/2)
    assert Rotation.D(Rational(3, 2), Rational(-1, 2), Rational(-1, 2), alpha, beta, gamma).doit() == \
        (cos(beta/2) + 3*cos(beta*Rational(3, 2)))/4*exp(I*alpha/2)*exp(I*gamma/2)
    assert Rotation.D(Rational(3, 2), Rational(-1, 2), Rational(-3, 2), alpha, beta, gamma).doit() == \
        -sqrt(3)*(sin(beta/2) + sin(beta*Rational(3, 2)))/4*exp(I*alpha/2)*exp(I*gamma*Rational(3, 2))
    assert Rotation.D(Rational(3, 2), Rational(-3, 2), Rational(3, 2), alpha, beta, gamma).doit() == \
        (3*sin(beta/2) - sin(beta*Rational(3, 2)))/4*exp(I*alpha*Rational(3, 2))*exp(I*gamma*Rational(-3, 2))
    assert Rotation.D(Rational(3, 2), Rational(-3, 2), S.Half, alpha, beta, gamma).doit() == \
        sqrt(3)*(cos(beta/2) - cos(beta*Rational(3, 2)))/4*exp(I*alpha*Rational(3, 2))*exp(-I*gamma/2)
    assert Rotation.D(Rational(3, 2), Rational(-3, 2), Rational(-1, 2), alpha, beta, gamma).doit() == \
        sqrt(3)*(sin(beta/2) + sin(beta*Rational(3, 2)))/4*exp(I*alpha*Rational(3, 2))*exp(I*gamma/2)
    assert Rotation.D(Rational(3, 2), Rational(-3, 2), Rational(-3, 2), alpha, beta, gamma).doit() == \
        (3*cos(beta/2) + cos(beta*Rational(3, 2)))/4*exp(I*alpha*Rational(3, 2))*exp(I*gamma*Rational(3, 2))
    # j = 2
    assert Rotation.D(2, 2, 2, alpha, beta, gamma).doit() == \
        (3 + 4*cos(beta) + cos(2*beta))/8*exp(-2*I*alpha)*exp(-2*I*gamma)
    assert Rotation.D(2, 2, 1, alpha, beta, gamma).doit() == \
        -((cos(beta) + 1)*exp(-2*I*alpha)*exp(-I*gamma)*sin(beta))/2
    assert Rotation.D(2, 2, 0, alpha, beta, gamma).doit() == \
        sqrt(6)*sin(beta)**2/4*exp(-2*I*alpha)
    assert Rotation.D(2, 2, -1, alpha, beta, gamma).doit() == \
        (cos(beta) - 1)*sin(beta)/2*exp(-2*I*alpha)*exp(I*gamma)
    assert Rotation.D(2, 2, -2, alpha, beta, gamma).doit() == \
        (3 - 4*cos(beta) + cos(2*beta))/8*exp(-2*I*alpha)*exp(2*I*gamma)
    assert Rotation.D(2, 1, 2, alpha, beta, gamma).doit() == \
        (cos(beta) + 1)*sin(beta)/2*exp(-I*alpha)*exp(-2*I*gamma)
    assert Rotation.D(2, 1, 1, alpha, beta, gamma).doit() == \
        (cos(beta) + cos(2*beta))/2*exp(-I*alpha)*exp(-I*gamma)
    assert Rotation.D(2, 1, 0, alpha, beta, gamma).doit() == -sqrt(6)* \
        sin(2*beta)/4*exp(-I*alpha)
    assert Rotation.D(2, 1, -1, alpha, beta, gamma).doit() == \
        (cos(beta) - cos(2*beta))/2*exp(-I*alpha)*exp(I*gamma)
    assert Rotation.D(2, 1, -2, alpha, beta, gamma).doit() == \
        (cos(beta) - 1)*sin(beta)/2*exp(-I*alpha)*exp(2*I*gamma)
    assert Rotation.D(2, 0, 2, alpha, beta, gamma).doit() == \
        sqrt(6)*sin(beta)**2/4*exp(-2*I*gamma)
    assert Rotation.D(2, 0, 1, alpha, beta, gamma).doit() == sqrt(6)* \
        sin(2*beta)/4*exp(-I*gamma)
    assert Rotation.D(
        2, 0, 0, alpha, beta, gamma).doit() == (1 + 3*cos(2*beta))/4
    assert Rotation.D(2, 0, -1, alpha, beta, gamma).doit() == -sqrt(6)* \
        sin(2*beta)/4*exp(I*gamma)
    assert Rotation.D(2, 0, -2, alpha, beta, gamma).doit() == \
        sqrt(6)*sin(beta)**2/4*exp(2*I*gamma)
    assert Rotation.D(2, -1, 2, alpha, beta, gamma).doit() == \
        (2*sin(beta) - sin(2*beta))/4*exp(I*alpha)*exp(-2*I*gamma)
    assert Rotation.D(2, -1, 1, alpha, beta, gamma).doit() == \
        (cos(beta) - cos(2*beta))/2*exp(I*alpha)*exp(-I*gamma)
    assert Rotation.D(2, -1, 0, alpha, beta, gamma).doit() == sqrt(6)* \
        sin(2*beta)/4*exp(I*alpha)
    assert Rotation.D(2, -1, -1, alpha, beta, gamma).doit() == \
        (cos(beta) + cos(2*beta))/2*exp(I*alpha)*exp(I*gamma)
    assert Rotation.D(2, -1, -2, alpha, beta, gamma).doit() == \
        -((cos(beta) + 1)*sin(beta))/2*exp(I*alpha)*exp(2*I*gamma)
    assert Rotation.D(2, -2, 2, alpha, beta, gamma).doit() == \
        (3 - 4*cos(beta) + cos(2*beta))/8*exp(2*I*alpha)*exp(-2*I*gamma)
    assert Rotation.D(2, -2, 1, alpha, beta, gamma).doit() == \
        (2*sin(beta) - sin(2*beta))/4*exp(2*I*alpha)*exp(-I*gamma)
    assert Rotation.D(2, -2, 0, alpha, beta, gamma).doit() == \
        sqrt(6)*sin(beta)**2/4*exp(2*I*alpha)
    assert Rotation.D(2, -2, -1, alpha, beta, gamma).doit() == \
        (cos(beta) + 1)*sin(beta)/2*exp(2*I*alpha)*exp(I*gamma)
    assert Rotation.D(2, -2, -2, alpha, beta, gamma).doit() == \
        (3 + 4*cos(beta) + cos(2*beta))/8*exp(2*I*alpha)*exp(2*I*gamma)
    # Numerical tests
    # j = 1/2
    assert Rotation.D(
        S.Half, S.Half, S.Half, pi/2, pi/2, pi/2).doit() == -I*sqrt(2)/2
    assert Rotation.D(
        S.Half, S.Half, Rational(-1, 2), pi/2, pi/2, pi/2).doit() == -sqrt(2)/2
    assert Rotation.D(
        S.Half, Rational(-1, 2), S.Half, pi/2, pi/2, pi/2).doit() == sqrt(2)/2
    assert Rotation.D(
        S.Half, Rational(-1, 2), Rational(-1, 2), pi/2, pi/2, pi/2).doit() == I*sqrt(2)/2
    # j = 1
    assert Rotation.D(1, 1, 1, pi/2, pi/2, pi/2).doit() == Rational(-1, 2)
    assert Rotation.D(1, 1, 0, pi/2, pi/2, pi/2).doit() == I*sqrt(2)/2
    assert Rotation.D(1, 1, -1, pi/2, pi/2, pi/2).doit() == S.Half
    assert Rotation.D(1, 0, 1, pi/2, pi/2, pi/2).doit() == -I*sqrt(2)/2
    assert Rotation.D(1, 0, 0, pi/2, pi/2, pi/2).doit() == 0
    assert Rotation.D(1, 0, -1, pi/2, pi/2, pi/2).doit() == -I*sqrt(2)/2
    assert Rotation.D(1, -1, 1, pi/2, pi/2, pi/2).doit() == S.Half
    assert Rotation.D(1, -1, 0, pi/2, pi/2, pi/2).doit() == I*sqrt(2)/2
    assert Rotation.D(1, -1, -1, pi/2, pi/2, pi/2).doit() == Rational(-1, 2)
    # j = 3/2
    assert Rotation.D(
        Rational(3, 2), Rational(3, 2), Rational(3, 2), pi/2, pi/2, pi/2).doit() == I*sqrt(2)/4
    assert Rotation.D(
        Rational(3, 2), Rational(3, 2), S.Half, pi/2, pi/2, pi/2).doit() == sqrt(6)/4
    assert Rotation.D(
        Rational(3, 2), Rational(3, 2), Rational(-1, 2), pi/2, pi/2, pi/2).doit() == -I*sqrt(6)/4
    assert Rotation.D(
        Rational(3, 2), Rational(3, 2), Rational(-3, 2), pi/2, pi/2, pi/2).doit() == -sqrt(2)/4
    assert Rotation.D(
        Rational(3, 2), S.Half, Rational(3, 2), pi/2, pi/2, pi/2).doit() == -sqrt(6)/4
    assert Rotation.D(
        Rational(3, 2), S.Half, S.Half, pi/2, pi/2, pi/2).doit() == I*sqrt(2)/4
    assert Rotation.D(
        Rational(3, 2), S.Half, Rational(-1, 2), pi/2, pi/2, pi/2).doit() == -sqrt(2)/4
    assert Rotation.D(
        Rational(3, 2), S.Half, Rational(-3, 2), pi/2, pi/2, pi/2).doit() == I*sqrt(6)/4
    assert Rotation.D(
        Rational(3, 2), Rational(-1, 2), Rational(3, 2), pi/2, pi/2, pi/2).doit() == -I*sqrt(6)/4
    assert Rotation.D(
        Rational(3, 2), Rational(-1, 2), S.Half, pi/2, pi/2, pi/2).doit() == sqrt(2)/4
    assert Rotation.D(
        Rational(3, 2), Rational(-1, 2), Rational(-1, 2), pi/2, pi/2, pi/2).doit() == -I*sqrt(2)/4
    assert Rotation.D(
        Rational(3, 2), Rational(-1, 2), Rational(-3, 2), pi/2, pi/2, pi/2).doit() == sqrt(6)/4
    assert Rotation.D(
        Rational(3, 2), Rational(-3, 2), Rational(3, 2), pi/2, pi/2, pi/2).doit() == sqrt(2)/4
    assert Rotation.D(
        Rational(3, 2), Rational(-3, 2), S.Half, pi/2, pi/2, pi/2).doit() == I*sqrt(6)/4
    assert Rotation.D(
        Rational(3, 2), Rational(-3, 2), Rational(-1, 2), pi/2, pi/2, pi/2).doit() == -sqrt(6)/4
    assert Rotation.D(
        Rational(3, 2), Rational(-3, 2), Rational(-3, 2), pi/2, pi/2, pi/2).doit() == -I*sqrt(2)/4
    # j = 2
    assert Rotation.D(2, 2, 2, pi/2, pi/2, pi/2).doit() == Rational(1, 4)
    assert Rotation.D(2, 2, 1, pi/2, pi/2, pi/2).doit() == -I/2
    assert Rotation.D(2, 2, 0, pi/2, pi/2, pi/2).doit() == -sqrt(6)/4
    assert Rotation.D(2, 2, -1, pi/2, pi/2, pi/2).doit() == I/2
    assert Rotation.D(2, 2, -2, pi/2, pi/2, pi/2).doit() == Rational(1, 4)
    assert Rotation.D(2, 1, 2, pi/2, pi/2, pi/2).doit() == I/2
    assert Rotation.D(2, 1, 1, pi/2, pi/2, pi/2).doit() == S.Half
    assert Rotation.D(2, 1, 0, pi/2, pi/2, pi/2).doit() == 0
    assert Rotation.D(2, 1, -1, pi/2, pi/2, pi/2).doit() == S.Half
    assert Rotation.D(2, 1, -2, pi/2, pi/2, pi/2).doit() == -I/2
    assert Rotation.D(2, 0, 2, pi/2, pi/2, pi/2).doit() == -sqrt(6)/4
    assert Rotation.D(2, 0, 1, pi/2, pi/2, pi/2).doit() == 0
    assert Rotation.D(2, 0, 0, pi/2, pi/2, pi/2).doit() == Rational(-1, 2)
    assert Rotation.D(2, 0, -1, pi/2, pi/2, pi/2).doit() == 0
    assert Rotation.D(2, 0, -2, pi/2, pi/2, pi/2).doit() == -sqrt(6)/4
    assert Rotation.D(2, -1, 2, pi/2, pi/2, pi/2).doit() == -I/2
    assert Rotation.D(2, -1, 1, pi/2, pi/2, pi/2).doit() == S.Half
    assert Rotation.D(2, -1, 0, pi/2, pi/2, pi/2).doit() == 0
    assert Rotation.D(2, -1, -1, pi/2, pi/2, pi/2).doit() == S.Half
    assert Rotation.D(2, -1, -2, pi/2, pi/2, pi/2).doit() == I/2
    assert Rotation.D(2, -2, 2, pi/2, pi/2, pi/2).doit() == Rational(1, 4)
    assert Rotation.D(2, -2, 1, pi/2, pi/2, pi/2).doit() == I/2
    assert Rotation.D(2, -2, 0, pi/2, pi/2, pi/2).doit() == -sqrt(6)/4
    assert Rotation.D(2, -2, -1, pi/2, pi/2, pi/2).doit() == -I/2
    assert Rotation.D(2, -2, -2, pi/2, pi/2, pi/2).doit() == Rational(1, 4)

