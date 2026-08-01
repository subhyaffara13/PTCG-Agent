
def restore_backend():
    """Restore the plotting backend to matplotlib"""
    with pandas.option_context("plotting.backend", "matplotlib"):
        yield

