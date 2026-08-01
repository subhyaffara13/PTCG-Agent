
def disable_gc():
    if gc.isenabled():
        try:
            gc.disable()
            yield
        finally:
            gc.enable()
    else:
        yield

