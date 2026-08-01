
def test_maybe_infer_to_datetimelike_df_construct(data, exp_size):
    result = DataFrame(np.array(data))
    assert result.size == exp_size

