
def test_issue_4527():
    k, m = symbols('k m', integer=True)
    assert integrate(sin(k*x)*sin(m*x), (x, 0, pi)).simplify() == \
        Piecewise((0, Eq(k, 0) | Eq(m, 0)),
                  (-pi/2, Eq(k, -m) | (Eq(k, 0) & Eq(m, 0))),
                  (pi/2, Eq(k, m) | (Eq(k, 0) & Eq(m, 0))),
                  (0, True))
    # Should be possible to further simplify to:
    # Piecewise(
    #    (0, Eq(k, 0) | Eq(m, 0)),
    #    (-pi/2, Eq(k, -m)),
    #    (pi/2, Eq(k, m)),
    #    (0, True))
    assert integrate(sin(k*x)*sin(m*x), (x,)) == Piecewise(
        (0, And(Eq(k, 0), Eq(m, 0))),
        (-x*sin(m*x)**2/2 - x*cos(m*x)**2/2 + sin(m*x)*cos(m*x)/(2*m), Eq(k, -m)),
        (x*sin(m*x)**2/2 + x*cos(m*x)**2/2 - sin(m*x)*cos(m*x)/(2*m), Eq(k, m)),
        (m*sin(k*x)*cos(m*x)/(k**2 - m**2) -
         k*sin(m*x)*cos(k*x)/(k**2 - m**2), True))

