
def test_byteswap():
    for val in (
        1,
        0x100,
        0x10000):
        a = np.array(val, dtype=np.uint32)
        b = a.byteswap()
        c = m5u.byteswap_u4(a)
        assert_equal(b.item(), c)
        d = m5u.byteswap_u4(c)
        assert_equal(a.item(), d)

