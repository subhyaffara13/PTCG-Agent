
def test_dynamic_attributes():
    instance = m.DynamicClass()
    assert not hasattr(instance, "foo")
    assert "foo" not in dir(instance)

    # Dynamically add attribute
    instance.foo = 42
    assert hasattr(instance, "foo")
    assert instance.foo == 42
    assert "foo" in dir(instance)

    # __dict__ should be accessible and replaceable
    assert "foo" in instance.__dict__
    instance.__dict__ = {"bar": True}
    assert not hasattr(instance, "foo")
    assert hasattr(instance, "bar")

    with pytest.raises(TypeError) as excinfo:
        instance.__dict__ = []
    assert str(excinfo.value) == "__dict__ must be set to a dictionary, not a 'list'"

    cstats = ConstructorStats.get(m.DynamicClass)
    assert cstats.alive() == 1
    del instance
    assert cstats.alive() == 0

    # Derived classes should work as well
    class PythonDerivedDynamicClass(m.DynamicClass):
        pass

    for cls in m.CppDerivedDynamicClass, PythonDerivedDynamicClass:
        derived = cls()
        derived.foobar = 100
        assert derived.foobar == 100

        assert cstats.alive() == 1
        del derived
        assert cstats.alive() == 0

