
def test_suppress_warnings_type():
    # NOTE(seberg): We test for the DeprecationWarning mainly because on
    # free-threaded Python an "ignore" warning filters seem to collide with
    # parts of what `suppress_warnings` does (if used more than once?).
    with pytest.warns(
            DeprecationWarning,
            match="suppression and assertion utilities are deprecated"):
        # Initial state of module, no warnings
        my_mod = _get_fresh_mod()
        assert_equal(getattr(my_mod, '__warningregistry__', {}), {})

        # Test module based warning suppression:
        with suppress_warnings() as sup:
            sup.filter(UserWarning)
            warnings.warn('Some warning')
        assert_warn_len_equal(my_mod, 0)
        sup = suppress_warnings()
        sup.filter(UserWarning)
        with sup:
            warnings.warn('Some warning')
        assert_warn_len_equal(my_mod, 0)
        # And test repeat works:
        sup.filter(module=my_mod)
        with sup:
            warnings.warn('Some warning')
        assert_warn_len_equal(my_mod, 0)

        # Without specified modules
        with suppress_warnings():
            warnings.simplefilter('ignore')
            warnings.warn('Some warning')
        assert_warn_len_equal(my_mod, 0)

