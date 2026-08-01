
def test_arg_min_max(rng, meth):
    ri = RangeIndex(rng)
    idx = Index(list(rng))
    assert getattr(ri, meth)() == getattr(idx, meth)()

