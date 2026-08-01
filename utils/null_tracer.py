
def null_tracer(name, **kwargs):
    """Context manager that yields a no-op span."""
    yield NullSpan()

