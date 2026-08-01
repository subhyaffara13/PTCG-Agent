
def test_multilevel_preserve_name(lexsorted_two_level_string_multiindex, indexer_sl):
    index = lexsorted_two_level_string_multiindex
    ser = Series(
        np.random.default_rng(2).standard_normal(len(index)), index=index, name="sth"
    )

    result = indexer_sl(ser)["foo"]
    assert result.name == ser.name

