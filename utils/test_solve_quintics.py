
def test_solve_quintics():
    skip("This test is too slow")
    f = x**5 - 110*x**3 - 55*x**2 + 2310*x + 979
    s = solveset_complex(f, x)
    for root in s:
        res = f.subs(x, root.n()).n()
        assert tn(res, 0)

    f = x**5 + 15*x + 12
    s = solveset_complex(f, x)
    for root in s:
        res = f.subs(x, root.n()).n()
        assert tn(res, 0)

