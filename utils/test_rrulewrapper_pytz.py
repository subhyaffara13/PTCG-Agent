
def test_rrulewrapper_pytz():
    # Test to make sure pytz zones are supported in rrules
    pytz = pytest.importorskip("pytz")

    def attach_tz(dt, zi):
        return zi.localize(dt)

    _test_rrulewrapper(attach_tz, pytz.timezone)

