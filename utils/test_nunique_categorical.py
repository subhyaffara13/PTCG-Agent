
def test_nunique_categorical():
    # GH#18051
    ser = Series(Categorical([]))
    assert ser.nunique() == 0

    ser = Series(Categorical([np.nan]))
    assert ser.nunique() == 0

