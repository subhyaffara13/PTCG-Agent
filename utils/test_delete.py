
def test_delete():
    df = DataFrame(
        np.random.default_rng(2).standard_normal((4, 3)), columns=["a", "b", "c"]
    )
    del df["b"]
    assert not df._mgr.blocks[0].refs.has_reference()
    assert not df._mgr.blocks[1].refs.has_reference()

    df = df[["a"]]
    assert not df._mgr.blocks[0].refs.has_reference()

