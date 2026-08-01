
def test_multiplication_initial_condition():
    x = symbols('x')
    R, Dx = DifferentialOperators(QQ.old_poly_ring(x), 'Dx')
    p = HolonomicFunction(Dx**2 + x*Dx - 1, x, 0, [3, 1])
    q = HolonomicFunction(Dx**2 + 1, x, 0, [1, 1])
    r = HolonomicFunction((x**4 + 14*x**2 + 60) + 4*x*Dx + (x**4 + 9*x**2 + 20)*Dx**2 + \
        (2*x**3 + 18*x)*Dx**3 + (x**2 + 10)*Dx**4, x, 0, [3, 4, 2, 3])
    assert p * q == r
    p = HolonomicFunction(Dx**2 + x, x, 0, [1, 0])
    q = HolonomicFunction(Dx**3 - x**2, x, 0, [3, 3, 3])
    r = HolonomicFunction((x**8 - 37*x**7/27 - 10*x**6/27 - 164*x**5/9 - 184*x**4/9 + \
        160*x**3/27 + 404*x**2/9 + 8*x + Rational(40, 3)) + (6*x**7 - 128*x**6/9 - 98*x**5/9 - 28*x**4/9 + \
        8*x**3/9 + 28*x**2 + x*Rational(40, 9) - 40)*Dx + (3*x**6 - 82*x**5/9 + 76*x**4/9 + 4*x**3/3 + \
        220*x**2/9 - x*Rational(80, 3))*Dx**2 + (-2*x**6 + 128*x**5/27 - 2*x**4/3 -80*x**2/9 + Rational(200, 9))*Dx**3 + \
        (3*x**5 - 64*x**4/9 - 28*x**3/9 + 6*x**2 - x*Rational(20, 9) - Rational(20, 3))*Dx**4 + (-4*x**3 + 64*x**2/9 + \
            x*Rational(8, 3))*Dx**5 + (x**4 - 64*x**3/27 - 4*x**2/3 + Rational(20, 9))*Dx**6, x, 0, [3, 3, 3, -3, -12, -24])
    assert p * q == r
    p = HolonomicFunction(Dx - 1, x, 0, [2])
    q = HolonomicFunction(Dx**2 + 1, x, 0, [0, 1])
    r = HolonomicFunction(2 -2*Dx + Dx**2, x, 0, [0, 2])
    assert p * q == r
    q = HolonomicFunction(x*Dx**2 + 1 + 2*Dx, x, 0,[0, 1])
    r = HolonomicFunction((x - 1) + (-2*x + 2)*Dx + x*Dx**2, x, 0, [0, 2])
    assert p * q == r
    p = HolonomicFunction(Dx**2 - 1, x, 0, [1, 3])
    q = HolonomicFunction(Dx**3 + 1, x, 0, [1, 2, 1])
    r = HolonomicFunction(6*Dx + 3*Dx**2 + 2*Dx**3 - 3*Dx**4 + Dx**6, x, 0, [1, 5, 14, 17, 17, 2])
    assert p * q == r
    p = expr_to_holonomic(sin(x))
    q = expr_to_holonomic(1/x, x0=1)
    r = HolonomicFunction(x + 2*Dx + x*Dx**2, x, 1, [sin(1), -sin(1) + cos(1)])
    assert p * q == r
    p = expr_to_holonomic(sqrt(x))
    q = expr_to_holonomic(sqrt(x**2-x))
    r = (p * q).to_expr()
    assert r == I*x*sqrt(-x + 1)

