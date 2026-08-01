
def test_find():
    expr = (x + y + 2 + sin(3*x))

    assert expr.find(lambda u: u.is_Integer) == {S(2), S(3)}
    assert expr.find(lambda u: u.is_Symbol) == {x, y}

    assert expr.find(lambda u: u.is_Integer, group=True) == {S(2): 1, S(3): 1}
    assert expr.find(lambda u: u.is_Symbol, group=True) == {x: 2, y: 1}

    assert expr.find(Integer) == {S(2), S(3)}
    assert expr.find(Symbol) == {x, y}

    assert expr.find(Integer, group=True) == {S(2): 1, S(3): 1}
    assert expr.find(Symbol, group=True) == {x: 2, y: 1}

    a = Wild('a')

    expr = sin(sin(x)) + sin(x) + cos(x) + x

    assert expr.find(lambda u: type(u) is sin) == {sin(x), sin(sin(x))}
    assert expr.find(
        lambda u: type(u) is sin, group=True) == {sin(x): 2, sin(sin(x)): 1}

    assert expr.find(sin(a)) == {sin(x), sin(sin(x))}
    assert expr.find(sin(a), group=True) == {sin(x): 2, sin(sin(x)): 1}

    assert expr.find(sin) == {sin(x), sin(sin(x))}
    assert expr.find(sin, group=True) == {sin(x): 2, sin(sin(x)): 1}


def test_find():
    keys = find('weak mixing', disp=False)
    assert_equal(keys, ['weak mixing angle'])

    keys = find('qwertyuiop', disp=False)
    assert_equal(keys, [])

    keys = find('natural unit', disp=False)
    assert_equal(keys, sorted(['natural unit of velocity',
                                'natural unit of action',
                                'natural unit of action in eV s',
                                'natural unit of mass',
                                'natural unit of energy',
                                'natural unit of energy in MeV',
                                'natural unit of momentum',
                                'natural unit of momentum in MeV/c',
                                'natural unit of length',
                                'natural unit of time']))


def test_find(code, result):
    code = _generate(dedent(code))
    if result is None:
        with pytest.raises(ValueError):
            _find(code, OP, ':')
    else:
        assert _find(code, OP, ':') == result


def test_find(any_string_dtype):
    ser = Series(
        ["ABCDEFG", "BCDEFEF", "DEFGHIJEF", "EFGHEF", "XXXX"], dtype=any_string_dtype
    )
    expected_dtype = (
        np.int64 if is_object_or_nan_string_dtype(any_string_dtype) else "Int64"
    )

    result = ser.str.find("EF")
    expected = Series([4, 3, 1, 0, -1], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)
    expected = np.array([v.find("EF") for v in np.array(ser)], dtype=np.int64)
    tm.assert_numpy_array_equal(np.array(result, dtype=np.int64), expected)

    result = ser.str.rfind("EF")
    expected = Series([4, 5, 7, 4, -1], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)
    expected = np.array([v.rfind("EF") for v in np.array(ser)], dtype=np.int64)
    tm.assert_numpy_array_equal(np.array(result, dtype=np.int64), expected)

    result = ser.str.find("EF", 3)
    expected = Series([4, 3, 7, 4, -1], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)
    expected = np.array([v.find("EF", 3) for v in np.array(ser)], dtype=np.int64)
    tm.assert_numpy_array_equal(np.array(result, dtype=np.int64), expected)

    result = ser.str.rfind("EF", 3)
    expected = Series([4, 5, 7, 4, -1], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)
    expected = np.array([v.rfind("EF", 3) for v in np.array(ser)], dtype=np.int64)
    tm.assert_numpy_array_equal(np.array(result, dtype=np.int64), expected)

    result = ser.str.find("EF", 3, 6)
    expected = Series([4, 3, -1, 4, -1], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)
    expected = np.array([v.find("EF", 3, 6) for v in np.array(ser)], dtype=np.int64)
    tm.assert_numpy_array_equal(np.array(result, dtype=np.int64), expected)

    result = ser.str.rfind("EF", 3, 6)
    expected = Series([4, 3, -1, 4, -1], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)
    expected = np.array([v.rfind("EF", 3, 6) for v in np.array(ser)], dtype=np.int64)
    tm.assert_numpy_array_equal(np.array(result, dtype=np.int64), expected)

