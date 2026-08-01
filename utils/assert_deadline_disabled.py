
def assert_deadline_disabled():
    """Check that deadlines are effectively disabled across Hypothesis versions."""
    if hypothesis_version < (3, 27, 0):
        import warnings

        warning_message = (
            "Your version of hypothesis is outdated. "
            "To avoid `DeadlineExceeded` errors, please update. "
            f"Current hypothesis version: {hypothesis.__version__}"
        )
        warnings.warn(warning_message, stacklevel=2)
    else:
        if settings().deadline is not None:
            raise AssertionError("Expected settings().deadline to be None")

