
def test_static_properties():
    assert m.TestProperties.def_readonly_static == 1
    with pytest.raises(AttributeError) as excinfo:
        m.TestProperties.def_readonly_static = 2
    assert NO_SETTER_MSG in str(excinfo.value)

    m.TestProperties.def_readwrite_static = 2
    assert m.TestProperties.def_readwrite_static == 2

    with pytest.raises(AttributeError) as excinfo:
        dummy = m.TestProperties.def_writeonly_static  # unused var
    assert NO_GETTER_MSG in str(excinfo.value)

    m.TestProperties.def_writeonly_static = 3
    assert m.TestProperties.def_readonly_static == 3

    assert m.TestProperties.def_property_readonly_static == 3
    with pytest.raises(AttributeError) as excinfo:
        m.TestProperties.def_property_readonly_static = 99
    assert NO_SETTER_MSG in str(excinfo.value)

    m.TestProperties.def_property_static = 4
    assert m.TestProperties.def_property_static == 4

    with pytest.raises(AttributeError) as excinfo:
        dummy = m.TestProperties.def_property_writeonly_static
    assert NO_GETTER_MSG in str(excinfo.value)

    m.TestProperties.def_property_writeonly_static = 5
    assert m.TestProperties.def_property_static == 5

    # Static property read and write via instance
    instance = m.TestProperties()

    m.TestProperties.def_readwrite_static = 0
    assert m.TestProperties.def_readwrite_static == 0
    assert instance.def_readwrite_static == 0

    instance.def_readwrite_static = 2
    assert m.TestProperties.def_readwrite_static == 2
    assert instance.def_readwrite_static == 2

    with pytest.raises(AttributeError) as excinfo:
        dummy = instance.def_property_writeonly_static  # noqa: F841 unused var
    assert NO_GETTER_MSG in str(excinfo.value)

    instance.def_property_writeonly_static = 4
    assert instance.def_property_static == 4

    # It should be possible to override properties in derived classes
    assert m.TestPropertiesOverride().def_readonly == 99
    assert m.TestPropertiesOverride.def_readonly_static == 99

    # Only static attributes can be deleted
    del m.TestPropertiesOverride.def_readonly_static
    assert hasattr(m.TestPropertiesOverride, "def_readonly_static")
    assert (
        m.TestPropertiesOverride.def_readonly_static
        is m.TestProperties.def_readonly_static
    )
    assert "def_readonly_static" not in m.TestPropertiesOverride.__dict__
    properties_override = m.TestPropertiesOverride()
    with pytest.raises(AttributeError) as excinfo:
        del properties_override.def_readonly
    assert NO_DELETER_MSG in str(excinfo.value)

