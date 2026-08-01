
def test_shift():
    assert Poly(x**2 - 2*x + 1, x).shift(2) == Poly(x**2 + 2*x + 1, x)


def test_shift(problem_func):
    A, b = problem_func()
    shift = 0.5
    shifted_A = A - shift * np.eye(10)
    x1, info1 = minres(A, b, shift=shift)
    x2, info2 = minres(shifted_A, b)
    assert_equal(info1, 0)
    assert_allclose(x1, x2, rtol=1e-5)


def test_shift(fill_value):
    ct = Categorical(
        ["a", "b", "c", "d"], categories=["a", "b", "c", "d"], ordered=False
    )
    expected = Categorical(
        [None, "a", "b", "c"], categories=["a", "b", "c", "d"], ordered=False
    )
    res = ct.shift(1, fill_value=fill_value)
    tm.assert_equal(res, expected)


def test_shift(idx):
    # GH8083 test the base class for shift
    msg = (
        "This method is only implemented for DatetimeIndex, PeriodIndex and "
        "TimedeltaIndex; Got type MultiIndex"
    )
    with pytest.raises(NotImplementedError, match=msg):
        idx.shift(1)
    with pytest.raises(NotImplementedError, match=msg):
        idx.shift(1, 2)

