
def test_tell_seek():
    with setup_test_file() as (fs, gs, cs):
        for s in (fs, gs, cs):
            st = make_stream(s)
            res = st.seek(0)
            assert_equal(res, 0)
            assert_equal(st.tell(), 0)
            res = st.seek(5)
            assert_equal(res, 0)
            assert_equal(st.tell(), 5)
            res = st.seek(2, 1)
            assert_equal(res, 0)
            assert_equal(st.tell(), 7)
            res = st.seek(-2, 2)
            assert_equal(res, 0)
            assert_equal(st.tell(), 6)

