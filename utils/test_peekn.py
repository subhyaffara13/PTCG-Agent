
def test_peekn():
    alist = ("Alice", "Bob", "Carol")
    elements, blist = peekn(2, alist)
    assert elements == alist[:2]
    assert tuple(blist) == alist

    elements, blist = peekn(len(alist) * 4, alist)
    assert elements == alist
    assert tuple(blist) == alist

