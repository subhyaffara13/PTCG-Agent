
def test_linprog():
    for do in range(2):
        if not do:
            M = lambda a, b: linear_eq_to_matrix(a, b)
        else:
            # check matrices as list
            M = lambda a, b: tuple([
                i.tolist() for i in linear_eq_to_matrix(a, b)])

        v = x, y, z = symbols('x1:4')
        f = x + y - 2*z
        c = M(f, v)[0]
        ineq = [7*x + 4*y - 7*z <= 3,
            3*x - y + 10*z <= 6,
            x >= 0, y >= 0, z >= 0]
        ab = M([i.lts - i.gts for i in ineq], v)
        ans = (-S(6)/5, [0, 0, S(3)/5])
        assert lpmin(f, ineq) == (ans[0], dict(zip(v, ans[1])))
        assert linprog(c, *ab) == ans

        f += 1
        c = M(f, v)[0]
        eq = [Eq(y - 9*x, 1)]
        abeq = M([i.lhs - i.rhs for i in eq], v)
        ans = (1 - S(2)/5, [0, 1, S(7)/10])
        assert lpmin(f, ineq + eq) == (ans[0], dict(zip(v, ans[1])))
        assert linprog(c, *ab, *abeq) == (ans[0] - 1, ans[1])

        eq = [z - y <= S.Half]
        abeq = M([i.lhs - i.rhs for i in eq], v)
        ans = (1 - S(10)/9, [0, S(1)/9, S(11)/18])
        assert lpmin(f, ineq + eq) == (ans[0], dict(zip(v, ans[1])))
        assert linprog(c, *ab, *abeq) == (ans[0] - 1, ans[1])

        bounds = [(0, None), (0, None), (None, S.Half)]
        ans = (0, [0, 0, S.Half])
        assert lpmin(f, ineq + [z <= S.Half]) == (
            ans[0], dict(zip(v, ans[1])))
        assert linprog(c, *ab, bounds=bounds) == (ans[0] - 1, ans[1])
        assert linprog(c, *ab, bounds={v.index(z): bounds[-1]}
            ) == (ans[0] - 1, ans[1])
        eq = [z - y <= S.Half]

    assert linprog([[1]], [], [], bounds=(2, 3)) == (2, [2])
    assert linprog([1], [], [], bounds=(2, 3)) == (2, [2])
    assert linprog([1], bounds=(2, 3)) == (2, [2])
    assert linprog([1, -1], [[1, 1]], [2], bounds={1:(None, None)}
        ) == (-2, [0, 2])
    assert linprog([1, -1], [[1, 1]], [5], bounds={1:(3, None)}
        ) == (-5, [0, 5])

