
def test_round_trip_conversion(notebook, fmt, update, allow_expected_differences=True, stop_on_first_error=True):
    """Test round trip conversion for a Jupyter notebook"""
    text = writes(notebook, fmt)
    round_trip = reads(text, fmt)

    if update:
        round_trip = combine_inputs_with_outputs(round_trip, notebook, fmt)

    compare_notebooks(
        round_trip,
        notebook,
        fmt,
        allow_expected_differences,
        raise_on_first_difference=stop_on_first_error,
    )

