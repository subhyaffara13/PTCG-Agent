
def test_factor_system_bool():

    eqs = [a*(x - 1)*(y - 1), b*(x - 2)*(y - 1)*(y - 2)]
    assert factor_system_bool(eqs, [x, y]) == (
        Eq(y - 1, 0)
        | (Eq(a, 0) & Eq(b, 0))
        | (Eq(a, 0) & Eq(x - 2, 0))
        | (Eq(a, 0) & Eq(y - 2, 0))
        | (Eq(b, 0) & Eq(x - 1, 0))
        | (Eq(x - 2, 0) & Eq(x - 1, 0))
        | (Eq(x - 1, 0) & Eq(y - 2, 0))
    )

    assert factor_system_bool([x - 1], [x]) == Eq(x - 1, 0)

    assert factor_system_bool([(x - 1)*(x - 2)], [x]) == Eq(x - 2, 0) | Eq(x - 1, 0)

    assert factor_system_bool([], [x]) == True
    assert factor_system_bool([0], [x]) == True
    assert factor_system_bool([1], [x]) == False
    assert factor_system_bool([a], [x]) == Eq(a, 0)

    assert factor_system_bool([a * x, y, a], [x, y]) == Eq(a, 0) & Eq(y, 0)

    assert (factor_system_bool([a*x, b*y*x, a], [x, y]) == (
        Eq(a, 0) & Eq(b, 0))
        | (Eq(a, 0) & Eq(x, 0))
        | (Eq(a, 0) & Eq(y, 0)))

    assert (factor_system_bool([a*x, b*x], [x, y]) == Eq(x, 0) |
            (Eq(a, 0) & Eq(b, 0)))

    assert (factor_system_bool([a*b*x, y], [x, y]) == (
        Eq(x, 0) & Eq(y, 0)) |
        (Eq(y, 0) & Eq(a*b, 0)))

    assert (factor_system_bool([a**2*x, y], [x, y]) == (
        Eq(a, 0) & Eq(y, 0)) |
        (Eq(x, 0) & Eq(y, 0)))

    assert factor_system_bool([a*x*y, b*y*z], [x, y, z]) == (
        Eq(y, 0)
        | (Eq(a, 0) & Eq(b, 0))
        | (Eq(a, 0) & Eq(z, 0))
        | (Eq(b, 0) & Eq(x, 0))
        | (Eq(x, 0) & Eq(z, 0))
    )

    assert factor_system_bool([a*(x - 1), b], [x]) == (
        (Eq(a, 0) & Eq(b, 0))
        | (Eq(x - 1, 0) & Eq(b, 0))
    )

