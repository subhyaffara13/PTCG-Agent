
def test_id_of_mapping(id, specification):
    uri = "http://example.com/some-schema"
    assert specification.id_of({id: uri}) == uri

