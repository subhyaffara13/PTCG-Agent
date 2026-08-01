
def test_specification_with_no_empty_fragment(uri, expected):
    assert referencing.jsonschema.specification_with(uri) == expected

