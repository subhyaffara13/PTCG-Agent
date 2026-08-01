
def test_list(capture, doc):
    assert m.list_no_args() == []
    assert m.list_ssize_t() == []
    assert m.list_size_t() == []
    lins = [1, 2]
    m.list_insert_ssize_t(lins)
    assert lins == [1, 83, 2]
    m.list_insert_size_t(lins)
    assert lins == [1, 83, 2, 57]

    with capture:
        lst = m.get_list()
        assert lst == ["inserted-0", "overwritten", "inserted-2"]

        lst.append("value2")
        m.print_list(lst)
    assert (
        capture.unordered
        == """
        Entry at position 0: value
        list item 0: inserted-0
        list item 1: overwritten
        list item 2: inserted-2
        list item 3: value2
    """
    )

    assert doc(m.get_list) == "get_list() -> list"
    assert doc(m.print_list) == "print_list(arg0: list) -> None"


def test_list():
    sT([x, Integer(4)], "[Symbol('x'), Integer(4)]")


def test_list():
    assert str([x]) == sstr([x]) == "[x]"
    assert str([x**2, x*y + 1]) == sstr([x**2, x*y + 1]) == "[x**2, x*y + 1]"
    assert str([x**2, [y + x]]) == sstr([x**2, [y + x]]) == "[x**2, [x + y]]"


def test_list(slice_test_df, slice_test_grouped, arg, expected_rows):
    # Test lists of integers and integer valued iterables
    result = slice_test_grouped._positional_selector[arg]
    expected = slice_test_df.iloc[expected_rows]

    tm.assert_frame_equal(result, expected)


def test_list():
    ser = ["1", "-3.14", "7"]
    res = to_numeric(ser)

    expected = np.array([1, -3.14, 7])
    tm.assert_numpy_array_equal(res, expected)

