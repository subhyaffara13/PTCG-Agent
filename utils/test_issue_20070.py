
def test_issue_20070():
    if not numba:
        skip("numba not installed")

    f = lambdify(x, sin(x), 'numpy')
    assert numba.jit(f, nopython=True)(1)==0.8414709848078965

