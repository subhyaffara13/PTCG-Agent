
def test_metadata_name():
    with pytest.raises(DistutilsSetupError, match='missing.*name'):
        Distribution()._validate_metadata()

