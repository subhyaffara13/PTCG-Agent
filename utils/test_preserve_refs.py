
def test_preserve_refs(datetime_series):
    seq = datetime_series.iloc[[5, 10, 15]]
    seq.iloc[1] = np.nan
    assert not np.isnan(datetime_series.iloc[10])

