
def test_issue_13167_21411():
    if not numpy:
        skip("numpy not installed")
    f1 = lambdify(x, sympy.Heaviside(x))
    f2 = lambdify(x, sympy.Heaviside(x, 1))
    res1 = f1([-1, 0, 1])
    res2 = f2([-1, 0, 1])
    assert Abs(res1[0]).n() < 1e-15        # First functionality: only one argument passed
    assert Abs(res1[1] - 1/2).n() < 1e-15
    assert Abs(res1[2] - 1).n() < 1e-15
    assert Abs(res2[0]).n() < 1e-15        # Second functionality: two arguments passed
    assert Abs(res2[1] - 1).n() < 1e-15
    assert Abs(res2[2] - 1).n() < 1e-15

