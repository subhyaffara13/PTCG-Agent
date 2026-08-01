
def test_loc_datetimelike_mismatched_dtypes():
    # GH#32650 dont mix and match datetime/timedelta/period dtypes

    df = DataFrame(
        np.random.default_rng(2).standard_normal((5, 3)),
        columns=["a", "b", "c"],
        index=date_range("2012", freq="h", periods=5),
    )
    # create dataframe with non-unique DatetimeIndex
    df = df.iloc[[0, 2, 2, 3]].copy()

    dti = df.index
    tdi = pd.TimedeltaIndex(dti.asi8)  # matching i8 values

    msg = r"None of \[TimedeltaIndex.* are in the \[index\]"
    with pytest.raises(KeyError, match=msg):
        df.loc[tdi]

    with pytest.raises(KeyError, match=msg):
        df["a"].loc[tdi]

