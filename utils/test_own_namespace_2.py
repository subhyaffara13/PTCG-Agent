
def test_own_namespace_2():
    def myfunc(x):
        return 1
    f = lambdify(x, sin(x), {'sin': myfunc})
    assert f(0.1) == 1
    assert f(100) == 1

