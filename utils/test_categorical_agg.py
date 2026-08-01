
def test_categorical_agg():
    # GH#36327
    values = np.random.default_rng(2).choice([1, 2, None], 30)
    df = pd.DataFrame(
        {"x": pd.Categorical(values, categories=[1, 2, 3]), "y": range(len(values))}
    )
    gb = df.groupby("x", dropna=False, observed=False)
    result = gb.agg(lambda x: x.sum())
    expected = gb.sum()
    tm.assert_frame_equal(result, expected)

