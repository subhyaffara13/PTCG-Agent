
def test_parent():
    x = [4,5,6,7]
    listiter = iter(x)
    obj = parent(listiter, list)
    assert obj is x

    if IS_PYPY: assert parent(obj, int) is None
    else: assert parent(obj, int) is x[-1] # python oddly? finds last int
    assert at(id(at)) is at

