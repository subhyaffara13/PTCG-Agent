
def test_make_stream():
    with setup_test_file() as (fs, gs, cs):
        # test stream initialization
        assert_(isinstance(make_stream(gs), GenericStream))

