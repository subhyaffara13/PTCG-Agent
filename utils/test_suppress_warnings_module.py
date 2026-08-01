
def test_suppress_warnings_module():
    # NOTE(seberg): We test for the DeprecationWarning mainly because on
    # free-threaded Python an "ignore" warning filters seem to collide with
    # parts of what `suppress_warnings` does (if used more than once?).
    with pytest.warns(
            DeprecationWarning,
            match="suppression and assertion utilities are deprecated"):
        # Initial state of module, no warnings
        my_mod = _get_fresh_mod()
        assert_equal(getattr(my_mod, '__warningregistry__', {}), {})

        def warn_other_module():
            # Apply along axis is implemented in python; stacklevel=2 means
            # we end up inside its module, not ours.
            def warn(arr):
                warnings.warn("Some warning 2", stacklevel=2)
                return arr
            np.apply_along_axis(warn, 0, [0])

        # Test module based warning suppression:
        assert_warn_len_equal(my_mod, 0)
        with suppress_warnings() as sup:
            sup.record(UserWarning)
            # suppress warning from other module (may have .pyc ending),
            # if apply_along_axis is moved, had to be changed.
            sup.filter(module=np.lib._shape_base_impl)
            warnings.warn("Some warning")
            warn_other_module()
        # Check that the suppression did test the file correctly (this module
        # got filtered)
        assert_equal(len(sup.log), 1)
        assert_equal(sup.log[0].message.args[0], "Some warning")
        assert_warn_len_equal(my_mod, 0)
        sup = suppress_warnings()
        # Will have to be changed if apply_along_axis is moved:
        sup.filter(module=my_mod)
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

