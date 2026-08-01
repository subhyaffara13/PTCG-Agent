
def test_array(doc):
    """std::array <-> list"""
    lst = m.cast_array()
    assert lst == [1, 2]
    assert m.load_array(lst)
    assert m.load_array(tuple(lst))

    assert doc(m.cast_array) == "cast_array() -> Annotated[List[int], FixedSize(2)]"
    assert (
        doc(m.load_array)
        == "load_array(arg0: Annotated[List[int], FixedSize(2)]) -> bool"
    )


def test_array(data, dtype, expected):
    result = pd.array(data, dtype=dtype)
    tm.assert_equal(result, expected)


def test_array(arr, attr, index_or_series):
    box = index_or_series

    result = box(arr, copy=False).array

    if attr:
        arr = getattr(arr, attr)
        result = getattr(result, attr)

    assert np.shares_memory(result, arr)

