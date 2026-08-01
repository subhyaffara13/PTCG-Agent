
def test_issue_5114_6611():
    # See that it doesn't hang; this solves in about 2 seconds.
    # Also check that the solution is relatively small.
    # Note: the system in issue 6611 solves in about 5 seconds and has
    # an op-count of 138336 (with simplify=False).
    b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r = symbols('b:r')
    eqs = Matrix([
        [b - c/d + r/d], [c*(1/g + 1/e + 1/d) - f/g - r/d],
        [-c/g + f*(1/j + 1/i + 1/g) - h/i], [-f/i + h*(1/m + 1/l + 1/i) - k/m],
        [-h/m + k*(1/p + 1/o + 1/m) - n/p], [-k/p + n*(1/q + 1/p)]])
    v = Matrix([f, h, k, n, b, c])
    ans = solve(list(eqs), list(v), simplify=False)
    # If time is taken to simplify then then 2617 below becomes
    # 1168 and the time is about 50 seconds instead of 2.
    assert sum(s.count_ops() for s in ans.values()) <= 3270

