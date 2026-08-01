
def test_rank_unordered_categorical_typeerror():
    # GH#51034 should be TypeError, not NotImplementedError
    cat = pd.Categorical([], ordered=False)
    ser = Series(cat)
    df = ser.to_frame()

    msg = "Cannot perform rank with non-ordered Categorical"

    gb = ser.groupby(cat, observed=False)
    with pytest.raises(TypeError, match=msg):
        gb.rank()

    gb2 = df.groupby(cat, observed=False)
    with pytest.raises(TypeError, match=msg):
        gb2.rank()

