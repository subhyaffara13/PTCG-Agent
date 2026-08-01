
def test_bad_encdoing_errors(temp_file):
    # GH 39777
    with pytest.raises(LookupError, match="unknown error handler name"):
        icom.get_handle(temp_file, "w", errors="bad")

