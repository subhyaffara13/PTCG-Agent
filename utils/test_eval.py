
def test_eval():
    assert Order(x).subs(Order(x), 1) == 1
    assert Order(x).subs(x, y) == Order(y)
    assert Order(x).subs(y, x) == Order(x)
    assert Order(x).subs(x, x + y) == Order(x + y, (x, -y))
    assert (O(1)**x).is_Pow


def test_eval():
    assert SingularityFunction(x, a, n).func == SingularityFunction
    assert unchanged(SingularityFunction, x, 5, n)
    assert SingularityFunction(5, 3, 2) == 4
    assert SingularityFunction(3, 5, 1) == 0
    assert SingularityFunction(3, 3, 0) == 1
    assert SingularityFunction(3, 3, 1) == 0
    assert SingularityFunction(Symbol('z', zero=True), 0, 1) == 0  # like sin(z) == 0
    assert SingularityFunction(4, 4, -1) is oo
    assert SingularityFunction(4, 2, -1) == 0
    assert SingularityFunction(4, 7, -1) == 0
    assert SingularityFunction(5, 6, -2) == 0
    assert SingularityFunction(4, 2, -2) == 0
    assert SingularityFunction(4, 4, -2) is oo
    assert SingularityFunction(4, 2, -3) == 0
    assert SingularityFunction(8, 8, -3) is oo
    assert SingularityFunction(4, 2, -4) == 0
    assert SingularityFunction(8, 8, -4) is oo
    assert (SingularityFunction(6.1, 4, 5)).evalf(5) == Float('40.841', '5')
    assert SingularityFunction(6.1, pi, 2) == (-pi + 6.1)**2
    assert SingularityFunction(x, a, nan) is nan
    assert SingularityFunction(x, nan, 1) is nan
    assert SingularityFunction(nan, a, n) is nan

    raises(ValueError, lambda: SingularityFunction(x, a, I))
    raises(ValueError, lambda: SingularityFunction(2*I, I, n))
    raises(ValueError, lambda: SingularityFunction(x, a, -5))


def test_eval():
    df = DataFrame({"a": [1, 2, 3], "b": 1})
    df_orig = df.copy()

    result = df.eval("c = a+b")
    assert np.shares_memory(get_array(df, "a"), get_array(result, "a"))

    result.iloc[0, 0] = 100
    tm.assert_frame_equal(df, df_orig)

