
def test_constructor_with_metadata_from_records():
    # GH#57008
    df = MySubclassWithMetadata.from_records([{"a": 1, "b": 2}])
    assert df.my_metadata is None
    assert type(df) is MySubclassWithMetadata

