
def test_is_list_like_generic():
    # GH 49649
    # is_list_like was yielding false positives for Generic classes in python 3.11
    T = TypeVar("T")

    class MyDataFrame(DataFrame, Generic[T]): ...

    tstc = MyDataFrame[int]
    tst = MyDataFrame[int]({"x": [1, 2, 3]})

    assert not inference.is_list_like(tstc)
    assert isinstance(tst, DataFrame)
    assert inference.is_list_like(tst)

