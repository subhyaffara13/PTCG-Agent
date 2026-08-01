
def test_issue_13961():
    V = (ax, bx, cx, gx, jx, lx, mx, nx, q) = symbols('ax bx cx gx jx lx mx nx q')
    S = (ax*q - lx*q - mx, ax - gx*q - lx, bx*q**2 + cx*q - jx*q - nx, q*(-ax*q + lx*q + mx), q*(-ax + gx*q + lx))

    sol = FiniteSet((lx + mx/q, (-cx*q + jx*q + nx)/q**2, cx, mx/q**2, jx, lx, mx, nx, Complement({q}, {0})),
                    (lx + mx/q, (cx*q - jx*q - nx)/q**2*-1, cx, mx/q**2, jx, lx, mx, nx, Complement({q}, {0})))
    assert nonlinsolve(S, *V) == sol

