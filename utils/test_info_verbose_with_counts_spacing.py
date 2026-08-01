
def test_info_verbose_with_counts_spacing(
    size, header_exp, separator_exp, first_line_exp, last_line_exp
):
    """Test header column, spacer, first line and last line in verbose mode."""
    frame = DataFrame(np.random.default_rng(2).standard_normal((3, size)))
    with StringIO() as buf:
        frame.info(verbose=True, show_counts=True, buf=buf)
        all_lines = buf.getvalue().splitlines()
    # Here table would contain only header, separator and table lines
    # dframe repr, index summary, memory usage and dtypes are excluded
    table = all_lines[3:-2]
    header, separator, first_line, *rest, last_line = table
    assert header == header_exp
    assert separator == separator_exp
    assert first_line == first_line_exp
    assert last_line == last_line_exp

