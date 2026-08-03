import functools

def skip_under_pyodide(message):
    """Decorator to skip a test if running under Pyodide/WASM."""
    def decorator(test_func):
        @functools.wraps(test_func)
        def test_wrapper():
            if IS_WASM:
                skip(message)
            return test_func()
        return test_wrapper
    return decorator

