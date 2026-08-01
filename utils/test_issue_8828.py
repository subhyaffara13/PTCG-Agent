
def test_issue_8828():
    x1 = 0
    y1 = -620
    r1 = 920
    x2 = 126
    y2 = 276
    x3 = 51
    y3 = 205
    r3 = 104
    v = x, y, z

    f1 = (x - x1)**2 + (y - y1)**2 - (r1 - z)**2
    f2 = (x - x2)**2 + (y - y2)**2 - z**2
    f3 = (x - x3)**2 + (y - y3)**2 - (r3 - z)**2
    F = f1,f2,f3

    g1 = sqrt((x - x1)**2 + (y - y1)**2) + z - r1
    g2 = f2
    g3 = sqrt((x - x3)**2 + (y - y3)**2) + z - r3
    G = g1,g2,g3

    A = solve(F, v)
    B = solve(G, v)
    C = solve(G, v, manual=True)

    p, q, r = [{tuple(i.evalf(2) for i in j) for j in R} for R in [A, B, C]]
    assert p == q == r


def test_issue_8828():
    x1 = 0
    y1 = -620
    r1 = 920
    x2 = 126
    y2 = 276
    x3 = 51
    y3 = 205
    r3 = 104
    v = [x, y, z]

    f1 = (x - x1)**2 + (y - y1)**2 - (r1 - z)**2
    f2 = (x2 - x)**2 + (y2 - y)**2 - z**2
    f3 = (x - x3)**2 + (y - y3)**2 - (r3 - z)**2
    F = [f1, f2, f3]

    g1 = sqrt((x - x1)**2 + (y - y1)**2) + z - r1
    g2 = f2
    g3 = sqrt((x - x3)**2 + (y - y3)**2) + z - r3
    G = [g1, g2, g3]

    # both soln same
    A = nonlinsolve(F, v)
    B = nonlinsolve(G, v)
    assert A == B

