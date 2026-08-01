
def test_nonlinsolve_complex():
    n = Dummy('n')
    assert dumeq(nonlinsolve([exp(x) - sin(y), 1/y - 3], [x, y]), {
        (ImageSet(Lambda(n, 2*n*I*pi + log(sin(Rational(1, 3)))), S.Integers), Rational(1, 3))})

    system = [exp(x) - sin(y), 1/exp(y) - 3]
    assert dumeq(nonlinsolve(system, [x, y]), {
        (ImageSet(Lambda(n, I*(2*n*pi + pi)
                         + log(sin(log(3)))), S.Integers), -log(3)),
        (ImageSet(Lambda(n, I*(2*n*pi + arg(sin(2*n*I*pi - log(3))))
                         + log(Abs(sin(2*n*I*pi - log(3))))), S.Integers),
        ImageSet(Lambda(n, 2*n*I*pi - log(3)), S.Integers))})

    system = [exp(x) - sin(y), y**2 - 4]
    assert dumeq(nonlinsolve(system, [x, y]), {
        (ImageSet(Lambda(n, I*(2*n*pi + pi) + log(sin(2))), S.Integers), -2),
        (ImageSet(Lambda(n, 2*n*I*pi + log(sin(2))), S.Integers), 2)})

    system = [exp(x) - 2, y ** 2 - 2]
    assert dumeq(nonlinsolve(system, [x, y]), {
        (log(2), -sqrt(2)), (log(2), sqrt(2)),
        (ImageSet(Lambda(n, 2*n*I*pi + log(2)), S.Integers), -sqrt(2)),
        (ImageSet(Lambda(n, 2 * n * I * pi + log(2)), S.Integers), sqrt(2))})

