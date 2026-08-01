
def test_clear_and_catch_warnings_inherit():
    # Test can subclass and add default modules
    my_mod = _get_fresh_mod()
    with my_cacw():
        warnings.simplefilter('ignore')
        warnings.warn('Some warning')
    assert_equal(my_mod.__warningregistry__, {})

