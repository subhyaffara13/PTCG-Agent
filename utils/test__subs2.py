
def test_Subs2():
    # this reflects a limitation of subs(), probably won't fix
    assert Subs(f(x), x**2, x).doit() == f(sqrt(x))

