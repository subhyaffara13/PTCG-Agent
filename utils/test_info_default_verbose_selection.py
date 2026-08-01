
def test_info_default_verbose_selection(num_columns, max_info_columns, verbose):
    frame = DataFrame(np.random.default_rng(2).standard_normal((5, num_columns)))
    with option_context("display.max_info_columns", max_info_columns):
        io_default = StringIO()
        frame.info(buf=io_default)
        result = io_default.getvalue()

        io_explicit = StringIO()
        frame.info(buf=io_explicit, verbose=verbose)
        expected = io_explicit.getvalue()

        assert result == expected

