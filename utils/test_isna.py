
def test_isna():
    assert pd.isna(NA) is True
    assert pd.notna(NA) is False

