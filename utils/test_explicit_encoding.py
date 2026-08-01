
def test_explicit_encoding(io_class, mode, msg):
    # GH39247; this test makes sure that if a user provides mode="*t" or "*b",
    # it is used. In the case of this test it leads to an error as intentionally the
    # wrong mode is requested
    expected = pd.DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=pd.Index(list("ABCD")),
        index=pd.Index([f"i-{i}" for i in range(30)]),
    )
    with io_class() as buffer:
        with pytest.raises(TypeError, match=msg):
            expected.to_csv(buffer, mode=f"w{mode}")

