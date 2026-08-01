
def test_suppress_warnings_decorate_no_record():
    # NOTE(seberg): We test for the DeprecationWarning mainly because on
    # free-threaded Python an "ignore" warning filters seem to collide with
    # parts of what `suppress_warnings` does (if used more than once?).
    with pytest.warns(
            DeprecationWarning,
            match="suppression and assertion utilities are deprecated"):
        sup = suppress_warnings()
        sup.filter(UserWarning)

        @sup
        def warn(category):
            warnings.warn('Some warning', category)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warn(UserWarning)  # should be suppressed
            warn(RuntimeWarning)
            assert_equal(len(w), 1)

