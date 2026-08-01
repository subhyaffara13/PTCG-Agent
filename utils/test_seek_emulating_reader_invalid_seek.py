
def test_seek_emulating_reader_invalid_seek():
    # Dummy data for the reader
    reader = wavfile.SeekEmulatingReader(BytesIO(b'\x00\x00'))
    
    # Test SEEK_END with an invalid whence value
    with pytest.raises(UnsupportedOperation):
        reader.seek(0, 5)  # Invalid whence value
    
    # Test with negative seek value
    with pytest.raises(UnsupportedOperation):
        reader.seek(-1, 0)  # Negative position with SEEK_SET
    
    # Test SEEK_END with valid parameters (should not raise)
    pos = reader.seek(0, os.SEEK_END)  # Valid usage
    assert pos == 2, f"Failed to seek to end, got position {pos}"

