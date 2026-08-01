
def test_Mul_is_nonpositive_nonnegative():
    x = Symbol('x', real=True)

    k = Symbol('k', negative=True)
    n = Symbol('n', positive=True)
    u = Symbol('u', nonnegative=True)
    v = Symbol('v', nonpositive=True)

    assert k.is_nonpositive is True
    assert (-k).is_nonpositive is False
    assert (2*k).is_nonpositive is True

    assert n.is_nonpositive is False
    assert (-n).is_nonpositive is True
    assert (2*n).is_nonpositive is False

    assert (n*k).is_nonpositive is True
    assert (2*n*k).is_nonpositive is True
    assert (-n*k).is_nonpositive is False

    assert u.is_nonpositive is None
    assert (-u).is_nonpositive is True
    assert (2*u).is_nonpositive is None

    assert v.is_nonpositive is True
    assert (-v).is_nonpositive is None
    assert (2*v).is_nonpositive is True

    assert (u*v).is_nonpositive is True

    assert (k*u).is_nonpositive is True
    assert (k*v).is_nonpositive is None

    assert (n*u).is_nonpositive is None
    assert (n*v).is_nonpositive is True

    assert (v*k*u).is_nonpositive is None
    assert (v*n*u).is_nonpositive is True

    assert (-v*k*u).is_nonpositive is True
    assert (-v*n*u).is_nonpositive is None

    assert (17*v*k*u).is_nonpositive is None
    assert (17*v*n*u).is_nonpositive is True

    assert (k*v*n*u).is_nonpositive is None

    assert (x*k).is_nonpositive is None
    assert (u*v*n*x*k).is_nonpositive is None

    assert k.is_nonnegative is False
    assert (-k).is_nonnegative is True
    assert (2*k).is_nonnegative is False

    assert n.is_nonnegative is True
    assert (-n).is_nonnegative is False
    assert (2*n).is_nonnegative is True

    assert (n*k).is_nonnegative is False
    assert (2*n*k).is_nonnegative is False
    assert (-n*k).is_nonnegative is True

    assert u.is_nonnegative is True
    assert (-u).is_nonnegative is None
    assert (2*u).is_nonnegative is True

    assert v.is_nonnegative is None
    assert (-v).is_nonnegative is True
    assert (2*v).is_nonnegative is None

    assert (u*v).is_nonnegative is None

    assert (k*u).is_nonnegative is None
    assert (k*v).is_nonnegative is True

    assert (n*u).is_nonnegative is True
    assert (n*v).is_nonnegative is None

    assert (v*k*u).is_nonnegative is True
    assert (v*n*u).is_nonnegative is None

    assert (-v*k*u).is_nonnegative is None
    assert (-v*n*u).is_nonnegative is True

    assert (17*v*k*u).is_nonnegative is True
    assert (17*v*n*u).is_nonnegative is None

    assert (k*v*n*u).is_nonnegative is True

    assert (x*k).is_nonnegative is None
    assert (u*v*n*x*k).is_nonnegative is None

