
def test_read():
    with setup_test_file() as (fs, gs, cs):
        for s in (fs, gs, cs):
            st = make_stream(s)
            st.seek(0)
            res = st.read(-1)
            assert_equal(res, b'a\x00string')
            st.seek(0)
            res = st.read(4)
            assert_equal(res, b'a\x00st')
            # read into
            st.seek(0)
            res = _read_into(st, 4)
            assert_equal(res, b'a\x00st')
            res = _read_into(st, 4)
            assert_equal(res, b'ring')
            assert_raises(OSError, _read_into, st, 2)
            # read alloc
            st.seek(0)
            res = _read_string(st, 4)
            assert_equal(res, b'a\x00st')
            res = _read_string(st, 4)
            assert_equal(res, b'ring')
            assert_raises(OSError, _read_string, st, 2)

