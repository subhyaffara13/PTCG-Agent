
def test_correct_arguments():
    raises(ValueError, lambda: R2.e_x(R2.e_x))
    raises(ValueError, lambda: R2.e_x(R2.dx))

    raises(ValueError, lambda: Commutator(R2.e_x, R2.x))
    raises(ValueError, lambda: Commutator(R2.dx, R2.e_x))

    raises(ValueError, lambda: Differential(Differential(R2.e_x)))

    raises(ValueError, lambda: R2.dx(R2.x))

    raises(ValueError, lambda: LieDerivative(R2.dx, R2.dx))
    raises(ValueError, lambda: LieDerivative(R2.x, R2.dx))

    raises(ValueError, lambda: CovarDerivativeOp(R2.dx, []))
    raises(ValueError, lambda: CovarDerivativeOp(R2.x, []))

    a = Symbol('a')
    raises(ValueError, lambda: intcurve_series(R2.dx, a, R2_r.point([1, 2])))
    raises(ValueError, lambda: intcurve_series(R2.x, a, R2_r.point([1, 2])))

    raises(ValueError, lambda: intcurve_diffequ(R2.dx, a, R2_r.point([1, 2])))
    raises(ValueError, lambda: intcurve_diffequ(R2.x, a, R2_r.point([1, 2])))

    raises(ValueError, lambda: contravariant_order(R2.e_x + R2.dx))
    raises(ValueError, lambda: covariant_order(R2.e_x + R2.dx))

    raises(ValueError, lambda: contravariant_order(R2.e_x*R2.e_y))
    raises(ValueError, lambda: covariant_order(R2.dx*R2.dy))

