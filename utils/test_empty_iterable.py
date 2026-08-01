
def test_empty_iterable():
    with pytest.raises(ValueError):
        index_satisfying([], lambda x: x > 0)

