
def test_savefig_metadata_error(fmt):
    with pytest.raises(ValueError, match="metadata not supported"):
        Figure().savefig(io.BytesIO(), format=fmt, metadata={})

