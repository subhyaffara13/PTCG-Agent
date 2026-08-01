
def test_getstate():
    from dill import dumps, loads
    dumps(f)
    b = bar[0]
    dumps(lambda: f, recurse=False) # doesn't call __getstate__
    assert bar[0] == b
    dumps(lambda: f, recurse=True) # calls __getstate__
    assert bar[0] == b + 1

