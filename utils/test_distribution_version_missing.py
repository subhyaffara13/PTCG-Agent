
def test_distribution_version_missing(
    tmpdir, suffix, expected_filename, expected_dist_type
):
    """
    Test Distribution.version when the "Version" header is missing.
    """
    basename = f'foo.{suffix}'
    dist, dist_dir = make_distribution_no_version(tmpdir, basename)

    expected_text = (
        f"Missing 'Version:' header and/or {expected_filename} file at path: "
    )
    metadata_path = os.path.join(dist_dir, expected_filename)

    # Now check the exception raised when the "version" attribute is accessed.
    with pytest.raises(ValueError) as excinfo:
        dist.version

    err = str(excinfo.value)
    # Include a string expression after the assert so the full strings
    # will be visible for inspection on failure.
    assert expected_text in err, str((expected_text, err))

    # Also check the args passed to the ValueError.
    msg, dist = excinfo.value.args
    assert expected_text in msg
    # Check that the message portion contains the path.
    assert metadata_path in msg, str((metadata_path, msg))
    assert type(dist) is expected_dist_type

