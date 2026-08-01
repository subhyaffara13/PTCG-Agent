
def test_equals_missing_values_differently_sorted():
    # GH#38439
    mi1 = MultiIndex.from_tuples([(81.0, np.nan), (np.nan, np.nan)])
    mi2 = MultiIndex.from_tuples([(np.nan, np.nan), (81.0, np.nan)])
    assert not mi1.equals(mi2)

    mi2 = MultiIndex.from_tuples([(81.0, np.nan), (np.nan, np.nan)])
    assert mi1.equals(mi2)

