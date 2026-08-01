
def test_is_array_like():
    assert inference.is_array_like(Series([], dtype=object))
    assert inference.is_array_like(Series([1, 2]))
    assert inference.is_array_like(np.array(["a", "b"]))
    assert inference.is_array_like(Index(["2016-01-01"]))
    assert inference.is_array_like(np.array([2, 3]))
    assert inference.is_array_like(MockNumpyLikeArray(np.array([2, 3])))

    class DtypeList(list):
        dtype = "special"

    assert inference.is_array_like(DtypeList())

    assert not inference.is_array_like([1, 2, 3])
    assert not inference.is_array_like(())
    assert not inference.is_array_like("foo")
    assert not inference.is_array_like(123)

