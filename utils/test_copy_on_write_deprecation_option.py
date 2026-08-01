
def test_copy_on_write_deprecation_option(value):
    msg = "Copy-on-Write can no longer be disabled"
    # stacklevel points to contextlib due to use of context manager.
    with tm.assert_produces_warning(Pandas4Warning, match=msg, check_stacklevel=False):
        with pd.option_context("mode.copy_on_write", value):
            pass

