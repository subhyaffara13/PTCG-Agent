
def test_import_error_message():
    # GH-19810
    df = DataFrame({"A": [1, 2]})

    with pytest.raises(ImportError, match="matplotlib is required for plotting"):
        df.plot()

