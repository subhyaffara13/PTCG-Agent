
def ignore_warns(expected_warning, *, match=None):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", match, expected_warning)
        yield

