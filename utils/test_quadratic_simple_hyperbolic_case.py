
def test_quadratic_simple_hyperbolic_case():
    # Simple Hyperbolic case: A = C = 0 and B != 0
    assert diop_solve(3*x*y + 34*x - 12*y + 1) == \
           {(-133, -11), (5, -57)}
    assert diop_solve(6*x*y + 2*x + 3*y + 1) == set()
    assert diop_solve(-13*x*y + 2*x - 4*y - 54) == {(27, 0)}
    assert diop_solve(-27*x*y - 30*x - 12*y - 54) == {(-14, -1)}
    assert diop_solve(2*x*y + 5*x + 56*y + 7) == {(-161, -3), (-47, -6), (-35, -12),
                                                  (-29, -69), (-27, 64), (-21, 7),
                                                  (-9, 1), (105, -2)}
    assert diop_solve(6*x*y + 9*x + 2*y + 3) == set()
    assert diop_solve(x*y + x + y + 1) == {(-1, t), (t, -1)}
    assert diophantine(48*x*y)

