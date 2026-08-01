
def tz(request):
    if isinstance(request.param, str) and request.param.startswith("pytz/"):
        pytz = pytest.importorskip("pytz")
        return pytz.timezone(request.param.removeprefix("pytz/"))
    return request.param

