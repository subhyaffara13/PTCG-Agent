
def test_issue_23318():
    eqs_eq = [
        Eq(53.5780461486929, x * log(y / (5.0 - y) + 1) / y),
        Eq(x, 0.0015 * z),
        Eq(0.0015, 7845.32 * y / z),
    ]
    eqs_expr = [eq.lhs - eq.rhs for eq in eqs_eq]

    sol = {(266.97755814852, 0.0340301680681629, 177985.03876568)}

    assert_close_nl(nonlinsolve(eqs_eq, [x, y, z]), sol)
    assert_close_nl(nonlinsolve(eqs_expr, [x, y, z]), sol)

    logterm = log(1.91196789933362e-7*z/(5.0 - 1.91196789933362e-7*z) + 1)
    eq = -0.0015*z*logterm + 1.02439504345316e-5*z
    assert_close_ss(solveset(eq, z), {0, 177985.038765679})

