
def test_groupby_quantile_with_arraylike_q_and_int_columns(frame_size, groupby, q):
    # GH30289
    nrow, ncol = frame_size
    df = DataFrame(np.array([ncol * [_ % 4] for _ in range(nrow)]), columns=range(ncol))

    idx_levels = [np.arange(min(nrow, 4))] * len(groupby) + [q]
    idx_codes = [[x for x in range(min(nrow, 4)) for _ in q]] * len(groupby) + [
        list(range(len(q))) * min(nrow, 4)
    ]
    expected_index = pd.MultiIndex(
        levels=idx_levels, codes=idx_codes, names=[*groupby, None]
    )
    expected_values = [
        [float(x)] * (ncol - len(groupby)) for x in range(min(nrow, 4)) for _ in q
    ]
    expected_columns = [x for x in range(ncol) if x not in groupby]
    expected = DataFrame(
        expected_values, index=expected_index, columns=expected_columns
    )
    result = df.groupby(groupby).quantile(q)

    tm.assert_frame_equal(result, expected)

