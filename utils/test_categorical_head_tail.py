
def test_categorical_head_tail(method, observed, sort, as_index):
    # GH#36327
    values = np.random.default_rng(2).choice([1, 2, None], 30)
    df = pd.DataFrame(
        {"x": pd.Categorical(values, categories=[1, 2, 3]), "y": range(len(values))}
    )
    gb = df.groupby("x", dropna=False, observed=observed, sort=sort, as_index=as_index)
    result = getattr(gb, method)()

    if method == "tail":
        values = values[::-1]
    # Take the top 5 values from each group
    mask = (
        ((values == 1) & ((values == 1).cumsum() <= 5))
        | ((values == 2) & ((values == 2).cumsum() <= 5))
        # flake8 doesn't like the vectorized check for None, thinks we should use `is`
        | ((values == None) & ((values == None).cumsum() <= 5))  # noqa: E711
    )
    if method == "tail":
        mask = mask[::-1]
    expected = df[mask]

    tm.assert_frame_equal(result, expected)

