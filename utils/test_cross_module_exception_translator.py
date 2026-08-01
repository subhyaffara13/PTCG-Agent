
def test_cross_module_exception_translator():
    with pytest.raises(KeyError):
        # translator registered in cross_module_tests
        m.throw_should_be_translated_to_key_error()

