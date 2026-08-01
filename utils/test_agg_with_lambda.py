
def test_agg_with_lambda(cases, agg):
    # passed lambda
    rcustom = cases["B"].apply(lambda x: np.std(x, ddof=1))
    expected = pd.concat([cases["A"].sum(), rcustom], axis=1)
    result = cases.agg(**agg)
    tm.assert_frame_equal(result, expected, check_like=True)

