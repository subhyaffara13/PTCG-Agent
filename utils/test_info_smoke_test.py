
def test_info_smoke_test(fixture_func_name, request):
    frame = request.getfixturevalue(fixture_func_name)
    buf = StringIO()
    frame.info(buf=buf)
    result = buf.getvalue().splitlines()
    assert len(result) > 10

    buf = StringIO()
    frame.info(buf=buf, verbose=False)

