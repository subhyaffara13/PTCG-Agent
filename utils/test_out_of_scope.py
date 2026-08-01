
def test_out_of_scope():
    def func():
        df = DataFrame({"a": [1, 2], "b": 1.5, "c": 1})
        # create some subset
        result = df[["a", "b"]]
        return result

    result = func()
    assert not result._mgr.blocks[0].refs.has_reference()
    assert not result._mgr.blocks[1].refs.has_reference()

