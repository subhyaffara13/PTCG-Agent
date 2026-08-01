
def test_read_magic_bad_magic():
    for magic in malformed_magic:
        f = BytesIO(magic)
        assert_raises(ValueError, format.read_array, f)

