
def test_output_buffer(mi_styler, format, temp_file):
    # gh 47053
    getattr(mi_styler, f"to_{format}")(temp_file)

