
def test_sparray_subscriptable():
    result = coo_array[np.int8, tuple[int]]
    assert isinstance(result, GenericAlias)
    assert result.__origin__ is coo_array
    assert result.__args__ == (np.int8, tuple[int])

    result = coo_array[np.int8]
    assert isinstance(result, GenericAlias)
    assert result.__origin__ is coo_array
    assert result.__args__ == (np.int8,)

