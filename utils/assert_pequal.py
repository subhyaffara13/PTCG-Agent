
def assert_pequal(a, b):
    a, b = [list(map(os.path.normpath, p)) for p in (a, b)]
    assert a == b

