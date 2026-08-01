
def test_read_hdf_generic_buffer_errors():
    msg = "Support for generic buffers has not been implemented."
    with pytest.raises(NotImplementedError, match=msg):
        read_hdf(BytesIO(b""), "df")

