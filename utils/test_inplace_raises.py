
def test_inplace_raises(method, frame_only):
    df = pd.DataFrame({"A": [0, 0], "B": [1, 2]}).set_flags(
        allows_duplicate_labels=False
    )
    s = df["A"]
    s.flags.allows_duplicate_labels = False
    msg = "Cannot specify"

    with pytest.raises(ValueError, match=msg):
        method(df)
    if not frame_only:
        with pytest.raises(ValueError, match=msg):
            method(s)

