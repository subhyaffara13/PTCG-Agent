
def test_to_dict_list_pd_scalars(val):
    # GH 54824
    df = DataFrame({"a": [val]})
    result = df.to_dict(orient="list")
    expected = {"a": [val]}
    assert result == expected

