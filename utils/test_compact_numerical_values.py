
def test_compact_numerical_values(datapath, column):
    # Regression test for #21616
    fname = datapath("io", "sas", "data", "cars.sas7bdat")
    df = pd.read_sas(fname, encoding="latin-1")
    # The two columns CYL and WGT in cars.sas7bdat have column
    # width < 8 and only contain integral values.
    # Test that pandas doesn't corrupt the numbers by adding
    # decimals.
    result = df[column]
    expected = df[column].round()
    tm.assert_series_equal(result, expected, check_exact=True)

