
def test_isnull_notnull_docstrings():
    # GH#41855 make sure its clear these are aliases
    doc = pd.DataFrame.notnull.__doc__
    assert doc.strip().startswith("DataFrame.notnull is an alias for DataFrame.notna.")
    doc = pd.DataFrame.isnull.__doc__
    assert doc.strip().startswith("DataFrame.isnull is an alias for DataFrame.isna.")

    doc = Series.notnull.__doc__
    assert doc.startswith("\nSeries.notnull is an alias for Series.notna.\n")
    doc = Series.isnull.__doc__
    assert doc.startswith("\nSeries.isnull is an alias for Series.isna.\n")

