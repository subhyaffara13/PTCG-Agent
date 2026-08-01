
def test_rle_rdc_exceptions(
    datapath, test_file, override_offset, override_value, expected_msg
):
    """Errors in RLE/RDC decompression should propagate."""
    with open(datapath("io", "sas", "data", test_file), "rb") as fd:
        data = bytearray(fd.read())
    data[override_offset] = override_value
    with pytest.raises(Exception, match=expected_msg):
        pd.read_sas(io.BytesIO(data), format="sas7bdat")

