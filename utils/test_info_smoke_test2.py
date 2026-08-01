
def test_info_smoke_test2(float_frame):
    # pretty useless test, used to be mixed into the repr tests
    buf = StringIO()
    float_frame.reindex(columns=["A"]).info(verbose=False, buf=buf)
    float_frame.reindex(columns=["A", "B"]).info(verbose=False, buf=buf)

    # no columns or index
    DataFrame().info(buf=buf)

