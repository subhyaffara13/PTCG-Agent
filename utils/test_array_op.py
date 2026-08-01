
def test_array_op(dtype, opname, exp):
    a = pd.array([1.0, 2.0, None, 4.0, 5.0], dtype=dtype)
    b = pd.array([0.1, 0.2, 0.3, None, 0.5], dtype=dtype)

    op = getattr(operator, opname)

    result = op(a, b)
    expected = pd.array(exp, dtype=dtype)
    tm.assert_extension_array_equal(result, expected)

