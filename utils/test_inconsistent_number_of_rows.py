
def test_inconsistent_number_of_rows(datapath):
    # Regression test for issue #16615. (PR #22628)
    fname = datapath("io", "sas", "data", "load_log.sas7bdat")
    df = pd.read_sas(fname, encoding="latin-1")
    assert len(df) == 2097

