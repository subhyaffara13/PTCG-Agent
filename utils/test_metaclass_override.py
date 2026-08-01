
def test_metaclass_override():
    """Overriding pybind11's default metaclass changes the behavior of `static_property`"""

    assert type(m.ExampleMandA).__name__ == "pybind11_type"
    assert type(m.MetaclassOverride).__name__ == "type"

    assert m.MetaclassOverride.readonly == 1
    assert (
        type(m.MetaclassOverride.__dict__["readonly"]).__name__
        == "pybind11_static_property"
    )

    # Regular `type` replaces the property instead of calling `__set__()`
    m.MetaclassOverride.readonly = 2
    assert m.MetaclassOverride.readonly == 2
    assert isinstance(m.MetaclassOverride.__dict__["readonly"], int)

