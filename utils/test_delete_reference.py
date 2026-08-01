
def test_delete_reference():
    df = DataFrame(
        np.random.default_rng(2).standard_normal((4, 3)), columns=["a", "b", "c"]
    )
    x = df[:]
    del df["b"]
    assert df._mgr.blocks[0].refs.has_reference()
    assert df._mgr.blocks[1].refs.has_reference()
    assert x._mgr.blocks[0].refs.has_reference()

