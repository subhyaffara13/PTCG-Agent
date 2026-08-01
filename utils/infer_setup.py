
def infer_setup(request):
    eastern, localize = request.param
    if isinstance(eastern, str) and eastern.startswith("pytz/"):
        pytz = pytest.importorskip("pytz")
        eastern = pytz.timezone(eastern.removeprefix("pytz/"))

    start_naive = datetime(2001, 1, 1)
    end_naive = datetime(2009, 1, 1)

    start = localize(eastern, start_naive)
    end = localize(eastern, end_naive)

    return eastern, localize, start, end, start_naive, end_naive

