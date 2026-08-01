
def test_schemas_with_explicit_schema_keywords_are_detected(uri, expected):
    """
    The $schema keyword in JSON Schema is a dialect identifier.
    """
    contents = {"$schema": uri}
    resource = Resource.from_contents(contents)
    assert resource == Resource(contents=contents, specification=expected)

