
def test_round():
    assert str(Float('0.1249999').round(2)) == '0.12'
    d20 = 12345678901234567890
    ans = S(d20).round(2)
    assert ans.is_Integer and ans == d20
    ans = S(d20).round(-2)
    assert ans.is_Integer and ans == 12345678901234567900
    assert str(S('1/7').round(4)) == '0.1429'
    assert str(S('.[12345]').round(4)) == '0.1235'
    assert str(S('.1349').round(2)) == '0.13'
    n = S(12345)
    ans = n.round()
    assert ans.is_Integer
    assert ans == n
    ans = n.round(1)
    assert ans.is_Integer
    assert ans == n
    ans = n.round(4)
    assert ans.is_Integer
    assert ans == n
    assert n.round(-1) == 12340

    r = Float(str(n)).round(-4)
    assert r == 10000.0

    assert n.round(-5) == 0

    assert str((pi + sqrt(2)).round(2)) == '4.56'
    assert (10*(pi + sqrt(2))).round(-1) == 50.0
    raises(TypeError, lambda: round(x + 2, 2))
    assert str(S(2.3).round(1)) == '2.3'
    # rounding in SymPy (as in Decimal) should be
    # exact for the given precision; we check here
    # that when a 5 follows the last digit that
    # the rounded digit will be even.
    for i in range(-99, 100):
        # construct a decimal that ends in 5, e.g. 123 -> 0.1235
        s = str(abs(i))
        p = len(s)  # we are going to round to the last digit of i
        n = '0.%s5' % s  # put a 5 after i's digits
        j = p + 2  # 2 for '0.'
        if i < 0:  # 1 for '-'
            j += 1
            n = '-' + n
        v = str(Float(n).round(p))[:j]  # pertinent digits
        if v.endswith('.'):
            continue  # it ends with 0 which is even
        L = int(v[-1])  # last digit
        assert L % 2 == 0, (n, '->', v)

    assert (Float(.3, 3) + 2*pi).round() == 7
    assert (Float(.3, 3) + 2*pi*100).round() == 629
    assert (pi + 2*E*I).round() == 3 + 5*I
    # don't let request for extra precision give more than
    # what is known (in this case, only 3 digits)
    assert str((Float(.03, 3) + 2*pi/100).round(5)) == '0.0928'
    assert str((Float(.03, 3) + 2*pi/100).round(4)) == '0.0928'

    assert S.Zero.round() == 0

    a = (Add(1, Float('1.' + '9'*27, ''), evaluate=False))
    assert a.round(10) == Float('3.000000000000000000000000000', '')
    assert a.round(25) == Float('3.000000000000000000000000000', '')
    assert a.round(26) == Float('3.000000000000000000000000000', '')
    assert a.round(27) == Float('2.999999999999999999999999999', '')
    assert a.round(30) == Float('2.999999999999999999999999999', '')
    #assert a.round(10) == Float('3.0000000000', '')
    #assert a.round(25) == Float('3.0000000000000000000000000', '')
    #assert a.round(26) == Float('3.00000000000000000000000000', '')
    #assert a.round(27) == Float('2.999999999999999999999999999', '')
    #assert a.round(30) == Float('2.999999999999999999999999999', '')

    # XXX: Should round set the precision of the result?
    #      The previous version of the tests above is this but they only pass
    #      because Floats with unequal precision compare equal:
    #
    # assert a.round(10) == Float('3.0000000000', '')
    # assert a.round(25) == Float('3.0000000000000000000000000', '')
    # assert a.round(26) == Float('3.00000000000000000000000000', '')
    # assert a.round(27) == Float('2.999999999999999999999999999', '')
    # assert a.round(30) == Float('2.999999999999999999999999999', '')

    raises(TypeError, lambda: x.round())
    raises(TypeError, lambda: f(1).round())

    # exact magnitude of 10
    assert str(S.One.round()) == '1'
    assert str(S(100).round()) == '100'

    # applied to real and imaginary portions
    assert (2*pi + E*I).round() == 6 + 3*I
    assert (2*pi + I/10).round() == 6
    assert (pi/10 + 2*I).round() == 2*I
    # the lhs re and im parts are Float with dps of 2
    # and those on the right have dps of 15 so they won't compare
    # equal unless we use string or compare components (which will
    # then coerce the floats to the same precision) or re-create
    # the floats
    assert str((pi/10 + E*I).round(2)) == '0.31 + 2.72*I'
    assert str((pi/10 + E*I).round(2).as_real_imag()) == '(0.31, 2.72)'
    assert str((pi/10 + E*I).round(2)) == '0.31 + 2.72*I'

    # issue 6914
    assert (I**(I + 3)).round(3) == Float('-0.208', '')*I

    # issue 8720
    assert S(-123.6).round() == -124
    assert S(-1.5).round() == -2
    assert S(-100.5).round() == -100
    assert S(-1.5 - 10.5*I).round() == -2 - 10*I

    # issue 7961
    assert str(S(0.006).round(2)) == '0.01'
    assert str(S(0.00106).round(4)) == '0.0011'

    # issue 8147
    assert S.NaN.round() is S.NaN
    assert S.Infinity.round() is S.Infinity
    assert S.NegativeInfinity.round() is S.NegativeInfinity
    assert S.ComplexInfinity.round() is S.ComplexInfinity

    # check that types match
    for i in range(2):
        fi = float(i)
        # 2 args
        assert all(type(round(i, p)) is int for p in (-1, 0, 1))
        assert all(S(i).round(p).is_Integer for p in (-1, 0, 1))
        assert all(type(round(fi, p)) is float for p in (-1, 0, 1))
        assert all(S(fi).round(p).is_Float for p in (-1, 0, 1))
        # 1 arg (p is None)
        assert type(round(i)) is int
        assert S(i).round().is_Integer
        assert type(round(fi)) is int
        assert S(fi).round().is_Integer

        # issue 25698
        n = 6000002
        assert int(n*(log(n) + log(log(n)))) == 110130079
        one = cos(2)**2 + sin(2)**2
        eq = exp(one*I*pi)
        qr, qi = eq.as_real_imag()
        assert qi.round(2) == 0.0
        assert eq.round(2) == -1.0
        eq = one - 1/S(10**120)
        assert S.true not in (eq > 1, eq < 1)
        assert int(eq) == int(.9) == 0
        assert int(-eq) == int(-.9) == 0


def test_round():
    msg = "type Expression doesn't define __round__ method"
    with pytest.raises(TypeError, match=msg):
        round(pd.col("a"), 2)


def test_round(decimals):
    df = DataFrame({"a": [1, 2], "b": "c"})
    df_orig = df.copy()
    df2 = df.round(decimals=decimals)

    assert tm.shares_memory(get_array(df2, "b"), get_array(df, "b"))
    # TODO: Make inplace by using out parameter of ndarray.round?
    if decimals >= 0 and Version(np.__version__) < Version("2.4.0.dev0"):
        # Ensure lazy copy if no-op
        # TODO: Cannot rely on Numpy returning view after version 2.3
        assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    else:
        assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    assert df2.index is not df.index
    assert df2.columns is not df.columns

    df2.iloc[0, 1] = "d"
    df2.iloc[0, 0] = 4
    assert not np.shares_memory(get_array(df2, "b"), get_array(df, "b"))
    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    tm.assert_frame_equal(df, df_orig)


def test_round():
    dtype = "float64[pyarrow]"

    ser = pd.Series([0.0, 1.23, 2.56, pd.NA], dtype=dtype)
    result = ser.round(1)
    expected = pd.Series([0.0, 1.2, 2.6, pd.NA], dtype=dtype)
    tm.assert_series_equal(result, expected)

    ser = pd.Series([123.4, pd.NA, 56.78], dtype=dtype)
    result = ser.round(-1)
    expected = pd.Series([120.0, pd.NA, 60.0], dtype=dtype)
    tm.assert_series_equal(result, expected)


def test_round(data, numpy_dtype):
    # No arguments
    result = data.round()
    np_result = np.round(data.to_numpy(dtype=numpy_dtype, na_value=None))
    exp_np = np_result.astype(object)
    exp_np[data.isna()] = pd.NA
    expected = pd.array(exp_np, dtype=data.dtype)
    tm.assert_extension_array_equal(result, expected)

    # Decimals argument
    result = data.round(decimals=2)
    np_result = np.round(data.to_numpy(dtype=numpy_dtype, na_value=None), decimals=2)
    exp_np = np_result.astype(object)
    exp_np[data.isna()] = pd.NA
    expected = pd.array(exp_np, dtype=data.dtype)
    tm.assert_extension_array_equal(result, expected)

