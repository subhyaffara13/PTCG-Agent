
def test_bad_magic_args():
    assert_raises(ValueError, format.magic, -1, 1)
    assert_raises(ValueError, format.magic, 256, 1)
    assert_raises(ValueError, format.magic, 1, -1)
    assert_raises(ValueError, format.magic, 1, 256)

