
def test_suppress_warnings_record():
    # NOTE(seberg): We test for the DeprecationWarning mainly because on
    # free-threaded Python an "ignore" warning filters seem to collide with
    # parts of what `suppress_warnings` does (if used more than once?).
    with pytest.warns(
            DeprecationWarning,
            match="suppression and assertion utilities are deprecated"):
        sup = suppress_warnings()
        log1 = sup.record()

        with sup:
            log2 = sup.record(message='Some other warning 2')
            sup.filter(message='Some warning')
            warnings.warn('Some warning')
            warnings.warn('Some other warning')
            warnings.warn('Some other warning 2')

            assert_equal(len(sup.log), 2)
            assert_equal(len(log1), 1)
            assert_equal(len(log2), 1)
            assert_equal(log2[0].message.args[0], 'Some other warning 2')

        # Do it again, with the same context to see if some warnings survived:
        with sup:
            log2 = sup.record(message='Some other warning 2')
            sup.filter(message='Some warning')
            warnings.warn('Some warning')
            warnings.warn('Some other warning')
            warnings.warn('Some other warning 2')

            assert_equal(len(sup.log), 2)
            assert_equal(len(log1), 1)
            assert_equal(len(log2), 1)
            assert_equal(log2[0].message.args[0], 'Some other warning 2')

        # Test nested:
        with suppress_warnings() as sup:
            sup.record()
            with suppress_warnings() as sup2:
                sup2.record(message='Some warning')
                warnings.warn('Some warning')
                warnings.warn('Some other warning')
                assert_equal(len(sup2.log), 1)
            # includes a DeprecationWarning for suppress_warnings
            assert_equal(len(sup.log), 2)

