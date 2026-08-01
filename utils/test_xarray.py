
def test_xarray(df):
    pytest.importorskip("xarray")

    assert df.to_xarray() is not None

