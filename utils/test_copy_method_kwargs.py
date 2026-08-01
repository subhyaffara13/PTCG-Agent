
def test_copy_method_kwargs(deep, kwarg, value):
    # gh-12309: Check that the "name" argument as well other kwargs are honored
    idx = MultiIndex(
        levels=[["foo", "bar"], ["fizz", "buzz"]],
        codes=[[0, 0, 0, 1], [0, 0, 1, 1]],
        names=["first", "second"],
    )
    idx_copy = idx.copy(**{kwarg: value, "deep": deep})
    assert getattr(idx_copy, kwarg) == value

