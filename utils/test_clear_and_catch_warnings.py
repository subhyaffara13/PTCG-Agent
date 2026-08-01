
def test_clear_and_catch_warnings():
    # Initial state of module, no warnings
    my_mod = _get_fresh_mod()
    assert_equal(getattr(my_mod, '__warningregistry__', {}), {})
    with clear_and_catch_warnings(modules=[my_mod]):
        warnings.simplefilter('ignore')
        warnings.warn('Some warning')
    assert_equal(my_mod.__warningregistry__, {})
    # Without specified modules, don't clear warnings during context.
    # catch_warnings doesn't make an entry for 'ignore'.
    with clear_and_catch_warnings():
        warnings.simplefilter('ignore')
        warnings.warn('Some warning')
    assert_warn_len_equal(my_mod, 0)

    # Manually adding two warnings to the registry:
    my_mod.__warningregistry__ = {'warning1': 1,
                                  'warning2': 2}

    # Confirm that specifying module keeps old warning, does not add new
    with clear_and_catch_warnings(modules=[my_mod]):
        warnings.simplefilter('ignore')
        warnings.warn('Another warning')
    assert_warn_len_equal(my_mod, 2)

    # Another warning, no module spec it clears up registry
    with clear_and_catch_warnings():
        warnings.simplefilter('ignore')
        warnings.warn('Another warning')
    assert_warn_len_equal(my_mod, 0)

