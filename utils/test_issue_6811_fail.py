
def test_issue_6811_fail():
    # from doc/src/modules/physics/mechanics/examples.rst, the current `eq`
    # at Line 576 (in different variables) was formerly the equivalent and
    # shorter expression given below...it would be nice to get the short one
    # back again
    xp, y, x, z = symbols('xp, y, x, z')
    eq = 4*(-19*sin(x)*y + 5*sin(3*x)*y + 15*cos(2*x)*z - 21*z)*xp/(9*cos(x) - 5*cos(3*x))
    assert trigsimp(eq) == -2*(2*cos(x)*tan(x)*y + 3*z)*xp/cos(x)

