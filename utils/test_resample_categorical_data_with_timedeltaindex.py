
def test_resample_categorical_data_with_timedeltaindex():
    # GH #12169
    df = DataFrame({"Group_obj": "A"}, index=pd.to_timedelta(list(range(20)), unit="s"))
    df["Group"] = df["Group_obj"].astype("category")
    result = df.resample("10s").agg(lambda x: x.value_counts().index[0])
    exp_tdi = pd.TimedeltaIndex(np.array([0, 10], dtype="m8[s]"), freq="10s")
    expected = DataFrame(
        {"Group_obj": ["A", "A"], "Group": ["A", "A"]},
        index=exp_tdi,
    )
    expected = expected.reindex(["Group_obj", "Group"], axis=1)
    expected["Group"] = expected["Group_obj"].astype("category")
    tm.assert_frame_equal(result, expected)

