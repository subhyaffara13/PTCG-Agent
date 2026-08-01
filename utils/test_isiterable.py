
def test_isiterable():
    # objects that have a __iter__() or __getitem__() method are iterable
    # https://docs.python.org/3/library/functions.html#iter
    class IterIterable:
        def __iter__(self):
            return iter(["a", "b", "c"])

    class GetItemIterable:
        def __getitem__(self, item):
            return ["a", "b", "c"][item]

    # "if a class sets __iter__() to None, the class is not iterable"
    # https://docs.python.org/3/reference/datamodel.html#special-method-names
    class NotIterable:
        __iter__ = None

    class NotIterableEvenWithGetItem:
        __iter__ = None

        def __getitem__(self, item):
            return ["a", "b", "c"][item]

    assert isiterable([1, 2, 3]) is True
    assert isiterable('abc') is True
    assert isiterable(IterIterable()) is True
    assert isiterable(GetItemIterable()) is True
    assert isiterable(5) is False
    assert isiterable(NotIterable()) is False
    assert isiterable(NotIterableEvenWithGetItem()) is False

