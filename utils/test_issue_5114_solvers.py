
def test_issue_5114_solvers():
    a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r = symbols('a:r')

    # there is no 'a' in the equation set but this is how the
    # problem was originally posed
    syms = a, b, c, f, h, k, n
    eqs = [b + r/d - c/d,
    c*(1/d + 1/e + 1/g) - f/g - r/d,
        f*(1/g + 1/i + 1/j) - c/g - h/i,
        h*(1/i + 1/l + 1/m) - f/i - k/m,
        k*(1/m + 1/o + 1/p) - h/m - n/p,
        n*(1/p + 1/q) - k/p]
    assert len(solve(eqs, syms, manual=True, check=False, simplify=False)) == 1

