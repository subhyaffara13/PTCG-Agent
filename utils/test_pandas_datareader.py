
def test_pandas_datareader():
    # https://github.com/pandas-dev/pandas/pull/61468
    # https://github.com/pydata/pandas-datareader/issues/1005
    pytest.importorskip("pandas_datareader")

