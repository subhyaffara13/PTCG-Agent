
def test_base_and_derived_nested_scope():
    assert issubclass(m.DerivedWithNested, m.BaseWithNested)
    assert m.BaseWithNested.Nested != m.DerivedWithNested.Nested
    assert m.BaseWithNested.Nested.get_name() == "BaseWithNested::Nested"
    assert m.DerivedWithNested.Nested.get_name() == "DerivedWithNested::Nested"

