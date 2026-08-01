
def test_ops_str_deprecated(box):
    # GH#59653
    td = Timedelta("1 day")
    item = "1"
    if box:
        item = np.array([item], dtype=object)

    msg = "Scalar operations between Timedelta and string are deprecated"
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        td + item
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        item + td
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        td - item
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        item - td
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        item / td
    if not box:
        with tm.assert_produces_warning(Pandas4Warning, match=msg):
            td / item
        with tm.assert_produces_warning(Pandas4Warning, match=msg):
            item // td
        with tm.assert_produces_warning(Pandas4Warning, match=msg):
            td // item
    else:
        msg = "|".join(
            [
                "ufunc 'divide' cannot use operands",
                "Invalid dtype object for __floordiv__",
                r"unsupported operand type\(s\) for /: 'int' and 'str'",
                r"unsupported operand type\(s\) for /: 'datetime.timedelta' and 'str'",
            ]
        )
        with pytest.raises(TypeError, match=msg):
            td / item
        with pytest.raises(TypeError, match=msg):
            item // td
        with pytest.raises(TypeError, match=msg):
            td // item

