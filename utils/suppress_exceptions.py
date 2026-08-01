
def suppress_exceptions(*excs):
    try:
        yield
    except excs:
        pass

