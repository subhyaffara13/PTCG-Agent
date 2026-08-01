
def test_product_rules():
    """
    Tests the six product rules defined with respect to the Del
    operator

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Del

    """

    #Define the scalar and vector functions
    f = 2*x*y*z
    g = x*y + y*z + z*x
    u = x**2*i + 4*j - y**2*z*k
    v = 4*i + x*y*z*k

    # First product rule
    lhs = delop(f * g, doit=True)
    rhs = (f * delop(g) + g * delop(f)).doit()
    assert simplify(lhs) == simplify(rhs)

    # Second product rule
    lhs = delop(u & v).doit()
    rhs = ((u ^ (delop ^ v)) + (v ^ (delop ^ u)) + \
          ((u & delop)(v)) + ((v & delop)(u))).doit()
    assert simplify(lhs) == simplify(rhs)

    # Third product rule
    lhs = (delop & (f*v)).doit()
    rhs = ((f * (delop & v)) + (v & (delop(f)))).doit()
    assert simplify(lhs) == simplify(rhs)

    # Fourth product rule
    lhs = (delop & (u ^ v)).doit()
    rhs = ((v & (delop ^ u)) - (u & (delop ^ v))).doit()
    assert simplify(lhs) == simplify(rhs)

    # Fifth product rule
    lhs = (delop ^ (f * v)).doit()
    rhs = (((delop(f)) ^ v) + (f * (delop ^ v))).doit()
    assert simplify(lhs) == simplify(rhs)

    # Sixth product rule
    lhs = (delop ^ (u ^ v)).doit()
    rhs = (u * (delop & v) - v * (delop & u) +
           (v & delop)(u) - (u & delop)(v)).doit()
    assert simplify(lhs) == simplify(rhs)

