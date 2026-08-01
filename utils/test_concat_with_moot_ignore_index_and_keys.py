
def test_concat_with_moot_ignore_index_and_keys():
    df1 = DataFrame([[0]])
    df2 = DataFrame([[42]])

    ignore_index = True
    keys = ["df1", "df2"]
    msg = f"Cannot set {ignore_index=} and specify keys. Either should be used."
    with pytest.raises(ValueError, match=msg):
        concat([df1, df2], keys=keys, ignore_index=ignore_index)

