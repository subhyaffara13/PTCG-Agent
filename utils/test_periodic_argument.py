
def test_periodic_argument():
    from sympy.functions.elementary.complexes import (periodic_argument, polar_lift, principal_branch, unbranched_argument)
    x = Symbol('x')
    p = Symbol('p', positive=True)

    assert unbranched_argument(2 + I) == periodic_argument(2 + I, oo)
    assert unbranched_argument(1 + x) == periodic_argument(1 + x, oo)
    assert N_equals(unbranched_argument((1 + I)**2), pi/2)
    assert N_equals(unbranched_argument((1 - I)**2), -pi/2)
    assert N_equals(periodic_argument((1 + I)**2, 3*pi), pi/2)
    assert N_equals(periodic_argument((1 - I)**2, 3*pi), -pi/2)

    assert unbranched_argument(principal_branch(x, pi)) == \
        periodic_argument(x, pi)

    assert unbranched_argument(polar_lift(2 + I)) == unbranched_argument(2 + I)
    assert periodic_argument(polar_lift(2 + I), 2*pi) == \
        periodic_argument(2 + I, 2*pi)
    assert periodic_argument(polar_lift(2 + I), 3*pi) == \
        periodic_argument(2 + I, 3*pi)
    assert periodic_argument(polar_lift(2 + I), pi) == \
        periodic_argument(polar_lift(2 + I), pi)

    assert unbranched_argument(polar_lift(1 + I)) == pi/4
    assert periodic_argument(2*p, p) == periodic_argument(p, p)
    assert periodic_argument(pi*p, p) == periodic_argument(p, p)

    assert Abs(polar_lift(1 + I)) == Abs(1 + I)

