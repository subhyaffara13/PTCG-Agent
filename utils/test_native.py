
def test_native():
    native_is_le = sys.byteorder == 'little'
    assert_(sibc.sys_is_le == native_is_le)

