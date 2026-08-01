
def test_apart_extension():
    f = 2/(x**2 + 1)
    g = I/(x + I) - I/(x - I)

    assert apart(f, extension=I) == g
    assert apart(f, gaussian=True) == g

    f = x/((x - 2)*(x + I))

    assert factor(together(apart(f)).expand()) == f

    f, g = _make_extension_example()

    # XXX: Only works with dotprodsimp. See test_apart_extension_xfail below
    from sympy.matrices import dotprodsimp
    with dotprodsimp(True):
        assert apart(f, x, extension={sqrt(2)}) == g

