
def test_empty_argmin_argmax_raises(meth):
    with pytest.raises(ValueError, match=f"attempt to get {meth} of an empty sequence"):
        getattr(RangeIndex(0), meth)()

