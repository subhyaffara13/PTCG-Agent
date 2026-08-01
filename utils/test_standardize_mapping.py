
def test_standardize_mapping():
    fill = {"bad": "data"}
    assert com.standardize_mapping(fill) == dict

    # Convert instance to type
    assert com.standardize_mapping({}) == dict

    dd = collections.defaultdict(list)
    assert isinstance(com.standardize_mapping(dd), partial)

