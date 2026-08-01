
def test_iterable(doc):
    assert doc(m.get_iterable) == "get_iterable() -> Iterable"


def test_iterable(value: t.Any) -> bool:
    """Check if it's possible to iterate over an object."""
    try:
        iter(value)
    except TypeError:
        return False

    return True


def test_iterable():
    assert iterable(0) is False
    assert iterable(1) is False
    assert iterable(None) is False

    class Test1(NotIterable):
        pass

    assert iterable(Test1()) is False

    class Test2(NotIterable):
        _iterable = True

    assert iterable(Test2()) is True

    class Test3:
        pass

    assert iterable(Test3()) is False

    class Test4:
        _iterable = True

    assert iterable(Test4()) is True

    class Test5:
        def __iter__(self):
            yield 1

    assert iterable(Test5()) is True

    class Test6(Test5):
        _iterable = False

    assert iterable(Test6()) is False

