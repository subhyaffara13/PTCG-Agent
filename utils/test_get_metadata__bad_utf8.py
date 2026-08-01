
def test_get_metadata__bad_utf8(tmpdir):
    """
    Test a metadata file with bytes that can't be decoded as utf-8.
    """
    filename = 'METADATA'
    # Convert the tmpdir LocalPath object to a string before joining.
    metadata_path = os.path.join(str(tmpdir), 'foo.dist-info', filename)
    # Encode a non-ascii string with the wrong encoding (not utf-8).
    metadata = 'née'.encode('iso-8859-1')
    dist = make_test_distribution(metadata_path, metadata=metadata)

    with pytest.raises(UnicodeDecodeError) as excinfo:
        dist.get_metadata(filename)

    exc = excinfo.value
    actual = str(exc)
    expected = (
        # The error message starts with "'utf-8' codec ..." However, the
        # spelling of "utf-8" can vary (e.g. "utf8") so we don't include it
        "codec can't decode byte 0xe9 in position 1: "
        'invalid continuation byte in METADATA file at path: '
    )
    assert expected in actual, f'actual: {actual}'
    assert actual.endswith(metadata_path), f'actual: {actual}'

