
def test_register_duplicate_class():
    import types

    module_scope = types.ModuleType("module_scope")
    with pytest.raises(RuntimeError) as exc_info:
        m.register_duplicate_class_name(module_scope)
    expected = (
        'generic_type: cannot initialize type "Duplicate": '
        "an object with that name is already defined"
    )
    assert str(exc_info.value) == expected
    with pytest.raises(RuntimeError) as exc_info:
        m.register_duplicate_class_type(module_scope)
    expected = 'generic_type: type "YetAnotherDuplicate" is already registered!'
    assert str(exc_info.value) == expected

    class ClassScope:
        pass

    with pytest.raises(RuntimeError) as exc_info:
        m.register_duplicate_nested_class_name(ClassScope)
    expected = (
        'generic_type: cannot initialize type "DuplicateNested": '
        "an object with that name is already defined"
    )
    assert str(exc_info.value) == expected
    with pytest.raises(RuntimeError) as exc_info:
        m.register_duplicate_nested_class_type(ClassScope)
    expected = 'generic_type: type "YetAnotherDuplicateNested" is already registered!'
    assert str(exc_info.value) == expected

