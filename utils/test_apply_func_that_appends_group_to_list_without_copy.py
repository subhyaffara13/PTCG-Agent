
def test_apply_func_that_appends_group_to_list_without_copy():
    # GH: 17718

    df = DataFrame(1, index=list(range(10)) * 10, columns=[0]).reset_index()
    groups = []

    def store(group):
        groups.append(group)

    df.groupby("index").apply(store)
    expected_value = DataFrame({0: [1] * 10}, index=pd.RangeIndex(0, 100, 10))
    expected_value.columns = expected_value.columns.astype(object)

    tm.assert_frame_equal(groups[0], expected_value)

