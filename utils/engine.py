
def engine(request):
    return request.param


def engine(request):
    if request.param == "numba":
        pytest.importorskip("numba")
    return request.param


def engine(request):
    return request.param


def engine(request):
    return request.param


def engine(request):
    return request.param


def engine(request):
    """engine keyword argument for rolling.apply"""
    return request.param


def engine(engine_and_read_ext):
    engine, read_ext = engine_and_read_ext
    return engine


def engine(request):
    if request.param == "pyarrow":
        pytest.importorskip("pyarrow.json")
    return request.param

