
def test_empty_pyarrow(data):
    # GH 53155
    pytest.importorskip("pyarrow", "14.0.0")
    from pyarrow.interchange import from_dataframe as pa_from_dataframe

    expected = pd.DataFrame(data)
    # Don't check stacklevel as PyArrow calls the deprecated `__dataframe__` method.
    with tm.assert_produces_warning(match="Interchange", check_stacklevel=False):
        arrow_df = pa_from_dataframe(expected)
    result = from_dataframe(arrow_df)
    tm.assert_frame_equal(result, expected, check_column_type=False)

