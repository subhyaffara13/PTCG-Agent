
def test_subresources_of_bool(specification, value):
    assert list(specification.subresources_of(value)) == []

