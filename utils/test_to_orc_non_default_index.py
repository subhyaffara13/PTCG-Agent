
def test_to_orc_non_default_index(index):
    df = pd.DataFrame({"a": [1, 2, 3]}, index=index)
    msg = (
        "orc does not support serializing a non-default index|"
        "orc does not serialize index meta-data"
    )
    with pytest.raises(ValueError, match=msg):
        df.to_orc()

