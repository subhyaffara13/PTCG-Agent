
def test_W22():
    t, u = symbols('t u', real=True)
    s = Lambda(x, Piecewise((1, And(x >= 1, x <= 2)), (0, True)))
    assert integrate(s(t)*cos(t), (t, 0, u)) == Piecewise(
        (0, u < 0),
        (-sin(Min(1, u)) + sin(Min(2, u)), True))

