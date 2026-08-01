
def test_peek():
    alist = ["Alice", "Bob", "Carol"]
    element, blist = peek(alist)
    assert element == alist[0]
    assert list(blist) == alist

    assert raises(StopIteration, lambda: peek([]))

