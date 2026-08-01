
def test_args_cnc():
    A = symbols('A', commutative=False)
    assert (x + A).args_cnc() == \
        [[], [x + A]]
    assert (x + a).args_cnc() == \
        [[a + x], []]
    assert (x*a).args_cnc() == \
        [[a, x], []]
    assert (x*y*A*(A + 1)).args_cnc(cset=True) == \
        [{x, y}, [A, 1 + A]]
    assert Mul(x, x, evaluate=False).args_cnc(cset=True, warn=False) == \
        [{x}, []]
    assert Mul(x, x**2, evaluate=False).args_cnc(cset=True, warn=False) == \
        [{x, x**2}, []]
    raises(ValueError, lambda: Mul(x, x, evaluate=False).args_cnc(cset=True))
    assert Mul(x, y, x, evaluate=False).args_cnc() == \
        [[x, y, x], []]
    # always split -1 from leading number
    assert (-1.*x).args_cnc() == [[-1, 1.0, x], []]

