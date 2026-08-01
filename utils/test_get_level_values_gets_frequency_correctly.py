
def test_get_level_values_gets_frequency_correctly():
    # GH#57949 GH#58327
    datetime_index = date_range(start=pd.to_datetime("1/1/2018"), periods=4, freq="YS")
    other_index = ["A"]
    multi_index = MultiIndex.from_product([datetime_index, other_index])

    assert multi_index.get_level_values(0).freq == datetime_index.freq

