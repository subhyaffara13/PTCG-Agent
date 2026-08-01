
def test_distribution_version_missing_undetected_path():
    """
    Test Distribution.version when the "Version" header is missing and
    the path can't be detected.
    """
    # Create a Distribution object with no metadata argument, which results
    # in an empty metadata provider.
    dist = Distribution('/foo')
    with pytest.raises(ValueError) as excinfo:
        dist.version

    msg, dist = excinfo.value.args
    expected = (
        "Missing 'Version:' header and/or PKG-INFO file at path: [could not detect]"
    )
    assert msg == expected

