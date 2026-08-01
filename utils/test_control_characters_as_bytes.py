
def test_control_characters_as_bytes():
    """Byte control characters (comments, delimiter) are supported."""
    a = np.loadtxt(StringIO("#header\n1,2,3"), comments=b"#", delimiter=b",")
    assert_equal(a, [1, 2, 3])

