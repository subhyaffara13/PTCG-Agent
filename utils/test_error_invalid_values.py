
def test_error_invalid_values(data, all_arithmetic_operators):
    # invalid ops
    op = all_arithmetic_operators
    s = pd.Series(data)
    ops = getattr(s, op)

    # invalid scalars
    msg = (
        "did not contain a loop with signature matching types|"
        "BooleanArray cannot perform the operation|"
        "not supported for the input types, and the inputs could not be safely coerced "
        "to any supported types according to the casting rule ''safe''|"
        "not supported for dtype"
    )
    with pytest.raises(TypeError, match=msg):
        ops("foo")
    msg = "|".join(
        [
            r"unsupported operand type\(s\) for",
            "Concatenation operation is not implemented for NumPy arrays",
            "has no kernel",
            "not supported for dtype",
        ]
    )
    with pytest.raises(TypeError, match=msg):
        ops(pd.Timestamp("20180101"))

    # invalid array-likes
    if op not in ("__mul__", "__rmul__"):
        # TODO(extension) numpy's mul with object array sees booleans as numbers
        msg = "|".join(
            [
                r"unsupported operand type\(s\) for",
                "can only concatenate str",
                "not all arguments converted during string formatting",
                "has no kernel",
                "not implemented",
                "not supported for dtype",
            ]
        )
        with pytest.raises(TypeError, match=msg):
            ops(pd.Series("foo", index=s.index))


def test_error_invalid_values(data, all_arithmetic_operators):
    op = all_arithmetic_operators
    s = pd.Series(data)
    ops = getattr(s, op)

    # invalid scalars
    msg = "|".join(
        [
            r"can only perform ops with numeric values",
            r"FloatingArray cannot perform the operation mod",
            "unsupported operand type",
            "not all arguments converted during string formatting",
            "can't multiply sequence by non-int of type 'float'",
            "ufunc 'subtract' cannot use operands with types dtype",
            r"can only concatenate str \(not \"float\"\) to str",
            "ufunc '.*' not supported for the input types, and the inputs could not",
            "ufunc '.*' did not contain a loop with signature matching types",
            "Concatenation operation is not implemented for NumPy arrays",
            "has no kernel",
            "not implemented",
            "not supported for dtype",
            "Can only string multiply by an integer",
        ]
    )
    with pytest.raises(TypeError, match=msg):
        ops("foo")
    with pytest.raises(TypeError, match=msg):
        ops(pd.Timestamp("20180101"))

    # invalid array-likes
    with pytest.raises(TypeError, match=msg):
        ops(pd.Series("foo", index=s.index))

    msg = "|".join(
        [
            "can only perform ops with numeric values",
            "cannot perform .* with this index type: DatetimeArray",
            "Addition/subtraction of integers and integer-arrays "
            "with DatetimeArray is no longer supported. *",
            "unsupported operand type",
            "not all arguments converted during string formatting",
            "can't multiply sequence by non-int of type 'float'",
            "ufunc 'subtract' cannot use operands with types dtype",
            (
                "ufunc 'add' cannot use operands with types "
                rf"dtype\('{tm.ENDIAN}M8\[ns\]'\)"
            ),
            r"ufunc 'add' cannot use operands with types dtype\('float\d{2}'\)",
            "cannot subtract DatetimeArray from ndarray",
            "has no kernel",
            "not implemented",
            "not supported for dtype",
        ]
    )
    with pytest.raises(TypeError, match=msg):
        ops(pd.Series(pd.date_range("20180101", periods=len(s), unit="ns")))


def test_error_invalid_values(data, all_arithmetic_operators):
    op = all_arithmetic_operators
    s = pd.Series(data)
    ops = getattr(s, op)

    # invalid scalars
    with tm.external_error_raised(TypeError):
        ops("foo")
    with tm.external_error_raised(TypeError):
        ops(pd.Timestamp("20180101"))

    # invalid array-likes
    str_ser = pd.Series("foo", index=s.index)
    # with pytest.raises(TypeError, match=msg):
    if all_arithmetic_operators in [
        "__mul__",
        "__rmul__",
    ]:  # (data[~data.isna()] >= 0).all():
        res = ops(str_ser)
        expected = pd.Series(["foo" * x for x in data], index=s.index)
        tm.assert_series_equal(res, expected)
    else:
        with tm.external_error_raised(TypeError):
            ops(str_ser)

    with tm.external_error_raised(TypeError):
        ops(pd.Series(pd.date_range("20180101", periods=len(s))))

