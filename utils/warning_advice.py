
def warning_advice(self, *args, **kwargs):
    """
    This method is identical to `logger.warning()`, but if env var TRANSFORMERS_NO_ADVISORY_WARNINGS=1 is set, this
    warning will not be printed
    """
    no_advisory_warnings = os.getenv("TRANSFORMERS_NO_ADVISORY_WARNINGS")
    if no_advisory_warnings:
        return
    self.warning(*args, **kwargs)

