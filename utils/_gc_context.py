
def _gc_context():
    is_enabled = gc.isenabled()
    gc.disable()
    try:
        yield
    finally:
        if is_enabled:
            gc.enable()

