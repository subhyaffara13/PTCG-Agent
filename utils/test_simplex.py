
def test_simplex():
    L = [
        [[1, 1], [-1, 1], [0, 1], [-1, 0]],
        [5, 1, 2, -1],
        [[1, 1]],
        [-1]]
    A, B, C, D = _abcd(_m(*L), list=False)
    assert _simplex(A, B, -C, -D) == (-6, [3, 2], [1, 0, 0, 0])
    assert _simplex(A, B, -C, -D, dual=True) == (-6,
        [1, 0, 0, 0], [5, 0])

    assert _simplex([[]],[],[[1]],[0]) == (0, [0], [])

    # handling of Eq (or Eq-like x<=y, x>=y conditions)
    assert lpmax(x - y, [x <= y + 2, x >= y + 2, x >= 0, y >= 0]
        ) == (2, {x: 2, y: 0})
    assert lpmax(x - y, [x <= y + 2, Eq(x, y + 2), x >= 0, y >= 0]
        ) == (2, {x: 2, y: 0})
    assert lpmax(x - y, [x <= y + 2, Eq(x, 2)]) == (2, {x: 2, y: 0})
    assert lpmax(y, [Eq(y, 2)]) == (2, {y: 2})

    # the conditions are equivalent to Eq(x, y + 2)
    assert lpmin(y, [x <= y + 2, x >= y + 2, y >= 0]
        ) == (0, {x: 2, y: 0})
    # equivalent to Eq(y, -2)
    assert lpmax(y, [0 <= y + 2, 0 >= y + 2]) == (-2, {y: -2})
    assert lpmax(y, [0 <= y + 2, 0 >= y + 2, y <= 0]
        ) == (-2, {y: -2})

    # extra symbols symbols
    assert lpmin(x, [y >= 1, x >= y]) == (1, {x: 1, y: 1})
    assert lpmin(x, [y >= 1, x >= y + z, x >= 0, z >= 0]
        ) == (1, {x: 1, y: 1, z: 0})

    # detect oscillation
    # o1
    v = x1, x2, x3, x4 = symbols('x1 x2 x3 x4')
    raises(InfeasibleLPError, lambda: lpmin(
        9*x2 - 8*x3 + 3*x4 + 6,
        [5*x2 - 2*x3 <= 0,
        -x1 - 8*x2 + 9*x3 <= -3,
        10*x1 - x2+ 9*x4 <= -4] + [i >= 0 for i in v]))
    # o2 - equations fed to lpmin are changed into a matrix
    # system that doesn't oscillate and has the same solution
    # as below
    M = linear_eq_to_matrix
    f = 5*x2 + x3 + 4*x4 - x1
    L = 5*x2 + 2*x3 + 5*x4 - (x1 + 5)
    cond = [L <= 0] + [Eq(3*x2 + x4, 2), Eq(-x1 + x3 + 2*x4, 1)]
    c, d = M(f, v)
    a, b = M(L, v)
    aeq, beq = M(cond[1:], v)
    ans = (S(9)/2, [0, S(1)/2, 0, S(1)/2])
    assert linprog(c, a, b, aeq, beq, bounds=(0, 1)) == ans
    lpans = lpmin(f, cond + [x1 >= 0, x1 <= 1,
        x2 >= 0, x2 <= 1, x3 >= 0, x3 <= 1, x4 >= 0, x4 <= 1])
    assert (lpans[0], list(lpans[1].values())) == ans

