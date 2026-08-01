
def test_specification_with(uri, expected):
    assert referencing.jsonschema.specification_with(uri) == expected

