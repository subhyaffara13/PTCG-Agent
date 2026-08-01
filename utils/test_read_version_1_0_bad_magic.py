
def test_read_version_1_0_bad_magic():
    for magic in bad_version_magic + malformed_magic:
        f = BytesIO(magic)
        assert_raises(ValueError, format.read_array, f)

