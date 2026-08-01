
def user_of_workers(x, b=1, workers=None):
    assert workers is not None
    assert isinstance(workers, MapWrapper)
    return np.array(list(workers(np.sin, x * b)))

