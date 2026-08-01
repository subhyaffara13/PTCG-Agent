
def test_trig_system_fail():
    # fails because solveset trig solver is not much smart.
    sys = [x + y - pi/2, sin(x) + sin(y) - 1]
    # solveset returns conditionset for sin(x) + sin(y) - 1
    soln_1 = (ImageSet(Lambda(n, n*pi + pi/2), S.Integers),
        ImageSet(Lambda(n, n*pi), S.Integers))
    soln_1 = FiniteSet(soln_1)
    soln_2 = (ImageSet(Lambda(n, n*pi), S.Integers),
        ImageSet(Lambda(n, n*pi+ pi/2), S.Integers))
    soln_2 = FiniteSet(soln_2)
    soln = soln_1 + soln_2
    assert dumeq(nonlinsolve(sys, [x, y]), soln)

    # Add more cases from here
    # http://www.vitutor.com/geometry/trigonometry/equations_systems.html#uno
    sys = [sin(x) + sin(y) - (sqrt(3)+1)/2, sin(x) - sin(y) - (sqrt(3) - 1)/2]
    soln_x = Union(ImageSet(Lambda(n, 2*n*pi + pi/3), S.Integers),
        ImageSet(Lambda(n, 2*n*pi + pi*Rational(2, 3)), S.Integers))
    soln_y = Union(ImageSet(Lambda(n, 2*n*pi + pi/6), S.Integers),
        ImageSet(Lambda(n, 2*n*pi + pi*Rational(5, 6)), S.Integers))
    assert dumeq(nonlinsolve(sys, [x, y]), FiniteSet((soln_x, soln_y)))

