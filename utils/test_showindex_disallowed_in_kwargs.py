
def test_showindex_disallowed_in_kwargs():
    # GH 32667; disallowing showindex in kwargs enforced in 2.0
    df = pd.DataFrame([1, 2, 3])
    with pytest.raises(ValueError, match="Pass 'index' instead of 'showindex"):
        df.to_markdown(index=True, showindex=True)

