
def test_DeferredVector():
    assert str(DeferredVector("vector")[4]) == "vector[4]"
    assert sympify(DeferredVector("d")) == DeferredVector("d")
    raises(IndexError, lambda: DeferredVector("d")[-1])
    assert str(DeferredVector("d")) == "d"
    assert repr(DeferredVector("test")) == "DeferredVector('test')"


def test_DeferredVector():
    assert str(DeferredVector("vector")[4]) == "vector[4]"
    assert sympify(DeferredVector("d")) == DeferredVector("d")
    raises(IndexError, lambda: DeferredVector("d")[-1])
    assert str(DeferredVector("d")) == "d"
    assert repr(DeferredVector("test")) == "DeferredVector('test')"

