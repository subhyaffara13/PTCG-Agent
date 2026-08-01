
def clear_backend_registry():
    # Fixture that clears the singleton backend_registry before and after use
    # so that the test state remains isolated.
    backend_registry._clear()
    yield
    backend_registry._clear()

